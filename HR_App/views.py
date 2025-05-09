import csv
import io
import os
import random
import re
import string
from itertools import chain
from operator import attrgetter
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction, models
from django.db.models import Prefetch, Sum, Value, CharField, F, Q
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from Project.models import Project,Task
from Timesheet.models import TaskRecord,ImagetaskRecord
from .models import EmployeeBISP, Leave, LeaveType, Designation, Department, HandbookPDF, \
    HandbookAcknowledgement, EmpLeaveType, EmployeeBISPHistory, LeaveTypeHistory, \
    LearningVideo, EmployeePersonalDetails, EmployeeEmergencyContact, EmployeeBankDetails, \
    EmployeeEducation, EmployeeExperience, EmployeeDocument  # Import your Employee model
from openpyxl import Workbook
from datetime import date, timedelta


# Create your views here.
def Manager(request):
    if request.session.get('role') != "Manager":
        return redirect("Login")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    employee = get_object_or_404(EmployeeBISP, id=employee_id, status='active')

    # Get all projects where the employee is admin or leader
    project_qs = Project.objects.filter(admin=employee,status='active') | Project.objects.filter(leader=employee,status='active')

    # Get related tasks from those projects
    task_qs = Task.objects.filter(assigned_to=employee,project__status='active')

    # Latest Handbook Message
    latest_pdf = HandbookPDF.objects.order_by('-uploaded_at').first()
    acknowledgement = None
    if latest_pdf:
        acknowledgement = HandbookAcknowledgement.objects.filter(employee=employee,
                                                                 pdf=latest_pdf).first()

    # Count tasks by status using simple logic
    status_counts = {
        'Pending': task_qs.filter(status='Pending').count(),
        'Inprogress': task_qs.filter(status='Inprogress').count(),
        'Claimed Completed': task_qs.filter(status='Claimed Completed').count(),
        'Completed': task_qs.filter(status='Completed').count(),
        'On Hold': task_qs.filter(status='On Hold').count(),
    }
    overdue_tasks = task_qs.exclude(status='Completed').count()
    total_tasks = task_qs.count()
    status_labels = ['Pending', 'Inprogress', 'Claimed Completed', 'Completed', 'On Hold']
    status_counts = {label: task_qs.filter(status=label).count() for label in status_labels}

    # Calculate percentage for each status
    status_percentages = {}
    for status, count in status_counts.items():
        status_percentages[status] = round((count / total_tasks) * 100, 2) if total_tasks else 0

    # Leave Summary for each leave type
    emp_leave_types = EmpLeaveType.objects.filter(employee=employee,leave_type__status = 'active')
    leave_summary = [
        {
            'leave_type': elt.leave_type.name,
            'total': elt.total_leave,
            'availed': elt.availed_leave,
            'remaining': elt.remaining_leave,
        }
        for elt in emp_leave_types
    ]

    # Aggregated leave totals
    aggregated_leave = emp_leave_types.aggregate(
        total_leave_sum=Sum('total_leave'),
        remaining_leave_sum=Sum('remaining_leave'),
        availed_leave_sum=Sum('availed_leave')
    )

    # Get all team members under the current manager
    team_member_ids = Project.objects.filter(leader=employee).values_list('team_members', flat=True).distinct()

    # Filter pending leaves for only those team members
    employee_leaves = Leave.objects.filter(
        status='Pending',
        employee__id__in=team_member_ids
    ).order_by('-created_at')[:5]

    # 1. Get projects where the logged-in manager is the leader
    led_projects = Project.objects.filter(leader=employee,status='active') | Project.objects.filter(admin=employee,status='active')

    # 2. Get employees who are team_members in those projects
    team_employees = EmployeeBISP.objects.filter(project_team__in=led_projects,status='active').distinct()

    # 3. Tasks claimed by these team members under manager's projects

    latest_tasks = Task.objects.filter(
        assigned_to__in=team_employees,
        status='Claimed Completed'
    ).annotate(
        activity_type=Value('Task', output_field=CharField())
    )

    self_tasks = Task.objects.filter(
        assigned_to=employee,
        status__in=['Completed', 'Pending']
    ).annotate(
        activity_type=Value('TaskSelf', output_field=CharField())
    )

    # 4. Leaves applied by these team members
    latest_leaves = Leave.objects.filter(
        Q(employee__in=team_employees) | Q(employee=employee)
    ).annotate(
        activity_type=Value('Leave', output_field=CharField())
    )

    # 5. Projects led by this manager
    latest_projects = led_projects.filter(
    status='Active'  # or exclude(status='Inactive') if there are multiple active statuses
    ).annotate(
        activity_type=Value('Project', output_field=CharField())
    )


    latest_projectCom = Project.objects.filter(
        Q(leader=employee) | Q(admin=employee),
        status='Inactive'  # or exclude(status='Inactive') if there are multiple active statuses
    ).annotate(
        activity_type=Value('ProjectCom', output_field=CharField())
    )


    latest_acknowledgements = HandbookAcknowledgement.objects.filter(
        employee__in=team_employees,
        status='Acknowledge'
    ).annotate(
        activity_type=Value('Handbook', output_field=CharField()),
        activity_datetime=F('acknowledged_at')
    ).select_related('employee', 'pdf')


    # Attach normalized datetime (prefer updated_at or fallback)
    for item in chain(latest_tasks, latest_leaves, latest_projects, latest_acknowledgements,latest_projectCom,self_tasks):
        if not hasattr(item, 'activity_datetime') or not item.activity_datetime:
            if hasattr(item, 'timestamp'):
                item.activity_datetime = item.timestamp
            elif hasattr(item, 'created_at'):
                item.activity_datetime = item.created_at
            elif hasattr(item, 'start_date'):
                item.activity_datetime = datetime.combine(item.start_date, time.min)
            elif hasattr(item, 'assigned_date'):
                item.activity_datetime = item.assigned_date
            else:
                item.activity_datetime = datetime.min

    # Combine and get latest 10
    combined_activities = sorted(
        chain(
            latest_tasks,
            latest_leaves,
            latest_projects,
            latest_acknowledgements,
            latest_projectCom,
            self_tasks,
        ),
        key=lambda x: x.activity_datetime,
        reverse=True
    )[:10]

    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee':EmployeeBISP.objects.filter(status='active').count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,
        'latest_activities': combined_activities,
        'team_employees':team_employees,
        'employee_leaves ':employee_leaves,
        'latest_pdf': latest_pdf,
        'acknowledgement': acknowledgement,

    }

    return render(request, 'admin_templates/index.html',context)


def Hr(request):
    # Ensure only Administrator can access
    if request.session.get('role') != "Administrator":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")
    employee = get_object_or_404(EmployeeBISP, id=employee_id, status='active')

    # Get all projects where the employee is admin or leader
    active_projects = Project.objects.filter(team_members__status='active',status='active')
    leader_projects = Project.objects.filter(leader__status='active',status='active')
    admin_projects = Project.objects.filter(admin__status='active',status='active')

    project_qs = (active_projects | leader_projects | admin_projects).distinct()

    #All Employee leave
    employee_leaves = Leave.objects.filter(status='Pending').order_by('-created_at')[:5]

    # Get related tasks from those projects
    task_qs = Task.objects.filter(project__status='active')

    # Get employees who are team members in those projects
    team_employees = EmployeeBISP.objects.filter(project_team__in=project_qs,status='active').distinct()

    # Count tasks by status using simple logic
    status_counts = {
        'Pending': task_qs.filter(status='Pending').count(),
        'Inprogress': task_qs.filter(status='Inprogress').count(),
        'Claimed Completed': task_qs.filter(status='Claimed Completed').count(),
        'Completed': task_qs.filter(status='Completed').count(),
        'On Hold': task_qs.filter(status='On Hold').count(),
    }

    overdue_tasks = task_qs.exclude(status='Completed').count()
    total_tasks = task_qs.count()
    status_labels = ['Pending', 'Inprogress', 'Claimed Completed', 'Completed', 'On Hold']
    status_counts = {label: task_qs.filter(status=label).count() for label in status_labels}

    # Calculate percentage for each status
    status_percentages = {}
    for status, count in status_counts.items():
        status_percentages[status] = round((count / total_tasks) * 100, 2) if total_tasks else 0

    # Leave Summary for each leave type
    emp_leave_types = EmpLeaveType.objects.filter(employee=employee,leave_type__status = 'active')
    leave_summary = [
        {
            'leave_type': elt.leave_type.name,
            'total': elt.total_leave,
            'availed': elt.availed_leave,
            'remaining': elt.remaining_leave,
        }
        for elt in emp_leave_types
    ]

    # Aggregated leave totals
    aggregated_leave = emp_leave_types.aggregate(
        total_leave_sum=Sum('total_leave'),
        remaining_leave_sum=Sum('remaining_leave'),
        availed_leave_sum=Sum('availed_leave')
    )

    # Latest Handbook Message
    latest_pdf = HandbookPDF.objects.order_by('-uploaded_at').first()
    acknowledgement = None
    if latest_pdf:
        acknowledgement = HandbookAcknowledgement.objects.filter(employee=employee,
                                                                 pdf=latest_pdf).first()


    # Annotate and fetch
    # Latest tasks
    latest_tasks = Task.objects.filter(
        assigned_to__isnull=False,
        status='Claimed Completed'
    ).annotate(
        activity_type=Value('Task', output_field=CharField())
    )

    # Latest leaves
    latest_leaves = Leave.objects.filter(employee__isnull=False).annotate(
        activity_type=Value('Leave', output_field=CharField())
    )

    # Latest projects (active)
    latest_projects = Project.objects.filter(
        team_members__isnull=False,
        status='Active'
    ).annotate(
        activity_type=Value('Project', output_field=CharField())
    )

    # Latest projects (inactive, for a specific employee)
    latest_projectCom = Project.objects.filter(
        status='Inactive'  # or exclude(status='Inactive') if there are multiple active statuses
    ).annotate(
        activity_type=Value('ProjectCom', output_field=CharField())
    )

    # Latest acknowledgements (acknowledged)
    latest_acknowledgements = HandbookAcknowledgement.objects.filter(
        status='Acknowledge'
    ).annotate(
        activity_type=Value('Handbook', output_field=CharField()),
        activity_datetime=F('acknowledged_at')  # Use actual acknowledgement datetime
    ).select_related('employee', 'pdf')


    # Normalize the datetime for other activities
    for item in chain(latest_tasks, latest_leaves, latest_projects, latest_acknowledgements, latest_projectCom):
        if not hasattr(item, 'activity_datetime') or not item.activity_datetime:
            if hasattr(item, 'timestamp'):
                item.activity_datetime = item.timestamp
            elif hasattr(item, 'created_at'):
                item.activity_datetime = item.created_at
            elif hasattr(item, 'start_date'):
                item.activity_datetime = datetime.combine(item.start_date, time.min)
            elif hasattr(item, 'assigned_date'):
                item.activity_datetime = item.assigned_date
            else:
                item.activity_datetime = datetime.min

    # Combine all activities and get the latest 10
    combined_activities = sorted(
        chain(
            latest_tasks,
            latest_leaves,
            latest_projects,
            latest_acknowledgements,
            latest_projectCom,
        ),
        key=lambda x: x.activity_datetime,
        reverse=True
    )[:10]
    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee': EmployeeBISP.objects.filter(status='active').count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,
        'employee_leaves': employee_leaves,
        'latest_activities': combined_activities,
        'team_employees':team_employees,
        'latest_pdf': latest_pdf,
        'acknowledgement': acknowledgement,

    }

    return render(request, 'admin_templates/hr_dashboard.html',context)


def Employee(request):
    if request.session.get('role') != "Employee":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    employee = get_object_or_404(EmployeeBISP, id=employee_id, status='active')

    # Get all projects where the employee is admin or leader
    project_qs = Project.objects.filter(team_members = employee,status='active')

    # Get related tasks from those projects
    task_qs = Task.objects.filter(assigned_to=employee,project__status='active')
    total_tasks = task_qs.count()
    status_labels = ['Pending', 'Inprogress', 'Claimed Completed', 'Completed', 'On Hold']
    status_counts = {label: task_qs.filter(status=label).count() for label in status_labels}
    # latest_tasks = Task.objects.select_related('assigned_to', 'project') \
    #                    .filter(assigned_to=employee) \
    #                    .order_by('-created_at')[:2]
    # latest_leaves = Leave.objects.filter(employee=employee).order_by('-created_at')[:2]
    # latest_projects = Project.objects.filter(team_members=employee).order_by('-created_at')[:2]

    # # Fetch latest items individually
    # latest_tasks = Task.objects.filter(assigned_to=employee).annotate(
    #     activity_type=models.Value('Task', output_field=models.CharField())).order_by('-created_at')[:5]
    # latest_leaves = Leave.objects.filter(employee=employee).annotate(
    #     activity_type=models.Value('Leave', output_field=models.CharField())).order_by('-start_date')[:5]
    # latest_projects = Project.objects.filter(team_members=employee).annotate(
    #     activity_type=models.Value('Project', output_field=models.CharField())).order_by('-created_at')[:5]
    #
    # # Combine and sort by date
    # combined_activities = sorted(
    #     chain(latest_tasks, latest_leaves, latest_projects),
    #     key=lambda x: getattr(x, 'created_at', getattr(x, 'start_date', getattr(x, 'assigned_date', None))),
    #     reverse=True
    # )

    # Latest Handbook Message
    latest_pdf = HandbookPDF.objects.order_by('-uploaded_at').first()
    acknowledgement = None
    if latest_pdf:
        acknowledgement = HandbookAcknowledgement.objects.filter(employee=employee,
                                                                 pdf=latest_pdf).first()

    # Calculate percentage for each status
    status_percentages = {}
    for status, count in status_counts.items():
        status_percentages[status] = round((count / total_tasks) * 100, 2) if total_tasks else 0

        # Leave Summary for each leave type
    emp_leave_types = EmpLeaveType.objects.filter(employee=employee,leave_type__status = 'active' )
    leave_summary = [
        {
            'leave_type': elt.leave_type.name,
            'total': elt.total_leave,
            'availed': elt.availed_leave,
            'remaining': elt.remaining_leave,
        }
        for elt in emp_leave_types
    ]

    # Aggregated leave totals
    aggregated_leave = emp_leave_types.aggregate(
        total_leave_sum=Sum('total_leave'),
        remaining_leave_sum=Sum('remaining_leave'),
        availed_leave_sum=Sum('availed_leave')
    )

    # Count tasks by status using simple logic
    status_counts = {
        'Pending': task_qs.filter(status='Pending').count(),
        'Inprogress': task_qs.filter(status='Inprogress').count(),
        'Claimed Completed': task_qs.filter(status='Claimed Completed').count(),
        'Completed': task_qs.filter(status='Completed').count(),
        'On Hold': task_qs.filter(status='On Hold').count(),
    }
    overdue_tasks = task_qs.filter(status__in=['Pending', 'Inprogress', 'Claimed Completed', 'On Hold']).count()

    # Annotate and fetch
    latest_tasks = Task.objects.filter(
        assigned_to=employee
    ).annotate(
        activity_type=Value('Task', output_field=CharField())
    )

    latest_leaves = Leave.objects.filter(employee=employee).annotate(
        activity_type=Value('Leave', output_field=CharField())
    )

    latest_projects = Project.objects.filter(
        team_members=employee,
        status = 'Active'
    ).annotate(
        activity_type=Value('Project', output_field=CharField())
    )
    latest_projectCom = Project.objects.filter(
        team_members=employee,
        status='Inactive'  # or exclude(status='Inactive') if there are multiple active statuses
    ).annotate(
        activity_type=Value('ProjectCom', output_field=CharField())
    )
    # Get all handbooks not yet acknowledged by the current employee
    # Latest handbooks (newly uploaded)
    latest_acknowledgements = HandbookPDF.objects.filter(
        uploaded_at__gt=F('timestamp')  # Ensure that the handbook is newly uploaded
    ).annotate(
        activity_type=Value('HandbookEmp', output_field=CharField()),
        activity_datetime=F('uploaded_at')  # Set the activity_datetime to uploaded_at
    ).order_by('-uploaded_at')  # Order by the most recent uploaded handbooks first

    # Attach normalized datetime (prefer updated_at or fallback)
    for item in chain(latest_tasks, latest_leaves, latest_projects,latest_acknowledgements,latest_projectCom):
        if hasattr(item, 'timestamp'):
            item.activity_datetime = item.timestamp
        elif hasattr(item, 'created_at'):
            item.activity_datetime = item.created_at
        elif hasattr(item, 'start_date'):
            item.activity_datetime = datetime.combine(item.start_date, time.min)
        elif hasattr(item, 'assigned_date'):
            item.activity_datetime = item.assigned_date
        else:
            item.activity_datetime = datetime.min  # fallback

    # Combine and get latest 10
    combined_activities = sorted(
        chain(latest_tasks, latest_leaves, latest_projects, latest_acknowledgements,latest_projectCom),
        key=lambda x: x.activity_datetime,
        reverse=True
    )[:10]

    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee': EmployeeBISP.objects.filter(status='active').count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,
        'latest_activities': combined_activities,
        'latest_pdf': latest_pdf,
        'acknowledgement': acknowledgement,

    }


    return render(request,'admin_templates/Emp_dashboard.html',context)

def Profile(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    today = date.today()
    monday_this_week = today - timedelta(days=today.weekday())  # Monday of current week
    monday_last_week = monday_this_week - timedelta(days=7)  # Monday of last week
    sunday_this_week = monday_this_week + timedelta(days=6)  # Sunday of current week

    # Week date list (optional for template display)
    dates = [monday_last_week + timedelta(days=i) for i in range(14)]

    # Get current employee
    employee_id = request.session.get('employee_id')
    employee = EmployeeBISP.objects.get(id=employee_id)
    # Leave Summary for each leave type
    emp_leave_types = EmpLeaveType.objects.filter(employee=employee,leave_type__status = 'active')

    leave_summary = [
        {
            'leave_type': elt.leave_type.name,
            'total': elt.total_leave,
            'availed': elt.availed_leave,
            'remaining': elt.remaining_leave,
        }
        for elt in emp_leave_types
    ]

    # Aggregated leave totals
    aggregated_leave = emp_leave_types.aggregate(
        total_leave_sum=Sum('total_leave'),
        remaining_leave_sum=Sum('remaining_leave'),
        availed_leave_sum=Sum('availed_leave')
    )


    # Filter TaskRecords where the task is assigned to current employee
    records = TaskRecord.objects.filter(
        task__assigned_to=employee,
        date__range=(monday_last_week, sunday_this_week)
    ).order_by('-date', '-start_time')

    # Calculate hours
    for record in records:
        if record.start_time and record.end_time:
            start_dt = datetime.combine(record.date, record.start_time)
            end_dt = datetime.combine(record.date, record.end_time)
            duration = end_dt - start_dt
            record.hours = round(duration.total_seconds() / 3600, 2)
        else:
            record.hours = 0

        # Check if the employee is an administrator
    if employee.role == 'Administrator':
        # Admin can see all projects
        projects = Project.objects.all().order_by('-created_at')

    elif employee.role == 'Manager':
        # Regular employees can only see projects they lead or are team members of
        projects = Project.objects.filter(leader=employee).order_by('-created_at') | Project.objects.filter(
            admin=employee).order_by('-created_at')
    else:
        projects = Project.objects.filter(team_members=employee).order_by('-created_at')

    if employee.role == 'Administrator':  # Assuming 'Administrator' is the role name in the field
        tasks = Task.objects.all().order_by('-created_at')  # Show all tasks if user is an admin
    else:
        tasks = Task.objects.filter(assigned_to=employee).order_by(
            '-created_at')  # Show only tasks assigned to the logged-in user

    try:
        # Get the employee record based on the logged-in user's email
        current_employee = EmployeeBISP.objects.prefetch_related(
            Prefetch(
                'leave_set',
                queryset=Leave.objects.all().order_by('-created_at')  # Order newest first
            )
        ).get(email=employee.email)
    except EmployeeBISP.DoesNotExist:
        messages.error(request, "Employee record not found.")

    try:
        employee = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        employee = None

    try:
        personalDetails=EmployeePersonalDetails.objects.filter(employee=employee).first()
    except EmployeePersonalDetails.DoesNotExist:
        personalDetails=None

    try:
        primary_contact = EmployeeEmergencyContact.objects.filter(employee=employee, priority=1).first()
    except EmployeeEmergencyContact.DoesNotExist:
        primary_contact=None

    try:
        secondary_contact = EmployeeEmergencyContact.objects.filter(employee=employee, priority=2).first()
    except EmployeeEmergencyContact.DoesNotExist:
        secondary_contact = None

    try:
        bank_details = EmployeeBankDetails.objects.filter(employee=employee).first()
    except EmployeeBankDetails.DoesNotExist:
        bank_details= None

    try:
        Edu =  EmployeeEducation.objects.filter(employee=employee).first()
    except EmployeeEducation.DoesNotExist:
       Edu= None

    try:
        PriExperience =EmployeeExperience.objects.filter(employee=employee,priority=1).first()
    except EmployeeExperience.DoesNotExist:
        PriExperience= None

    try:
        SecExperience =EmployeeExperience.objects.filter(employee=employee,priority=2).first()
    except EmployeeExperience.DoesNotExist:
        SecExperience= None

    try:
        Document =EmployeeDocument.objects.filter(employee=employee)
    except EmployeeDocument.DoesNotExist:
        Document= None

    return render(request,'admin_templates/profile.html',{'employee':employee,'records': records,'projects': projects.distinct(),'tasks': tasks,'employees': [current_employee],'personalDetails':personalDetails,'primary_contact': primary_contact,'secondary_contact':secondary_contact,'bank_details':bank_details,'Edu':Edu,'PriExperience':PriExperience,'SecExperience':SecExperience,'Document':Document,'total_leave':aggregated_leave})

#Profile of team member for administrator and manager
def Team_profile(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')


    today = date.today()
    monday_this_week = today - timedelta(days=today.weekday())  # Monday of current week
    monday_last_week = monday_this_week - timedelta(days=7)  # Monday of last week
    sunday_this_week = monday_this_week + timedelta(days=6)  # Sunday of current week


    try:
        employee = EmployeeBISP.objects.get(id=id)
    except EmployeeBISP.DoesNotExist:
        employee = None

    # Leave Summary for each leave type
    emp_leave_types = EmpLeaveType.objects.filter(employee=employee, leave_type__status='active')

    leave_summary = [
            {
                'leave_type': elt.leave_type.name,
                'total': elt.total_leave,
                'availed': elt.availed_leave,
                'remaining': elt.remaining_leave,
            }
            for elt in emp_leave_types
        ]

    # Aggregated leave totals
    aggregated_leave = emp_leave_types.aggregate(
            total_leave_sum=Sum('total_leave'),
            remaining_leave_sum=Sum('remaining_leave'),
            availed_leave_sum=Sum('availed_leave')
        )

        # Filter TaskRecords where the task is assigned to current employee
    records = TaskRecord.objects.filter(
        task__assigned_to=employee,
        date__range=(monday_last_week, sunday_this_week)
    ).order_by('-date', '-start_time')

    # Calculate hours
    for record in records:
        if record.start_time and record.end_time:
            start_dt = datetime.combine(record.date, record.start_time)
            end_dt = datetime.combine(record.date, record.end_time)
            duration = end_dt - start_dt
            record.hours = round(duration.total_seconds() / 3600, 2)
        else:
            record.hours = 0

        # Check if the employee is an administrator
    if employee.role == 'Administrator':
        # Admin can see all projects
        projects = Project.objects.all().order_by('-created_at')

    elif employee.role == 'Manager':
        # Regular employees can only see projects they lead or are team members of
        projects = Project.objects.filter(leader=employee).order_by('-created_at') | Project.objects.filter(
            admin=employee).order_by('-created_at')
    else:
        projects = Project.objects.filter(team_members=employee).order_by('-created_at')

    if employee.role == 'Administrator':  # Assuming 'Administrator' is the role name in the field
        tasks = Task.objects.all().order_by('-created_at')  # Show all tasks if user is an admin
    else:
        tasks = Task.objects.filter(assigned_to=employee).order_by(
            '-created_at')  # Show only tasks assigned to the logged-in user

    try:
        # Get the employee record based on the logged-in user's email
        current_employee = EmployeeBISP.objects.prefetch_related(
            Prefetch(
                'leave_set',
                queryset=Leave.objects.all().order_by('-created_at')  # Order newest first
            )
        ).get(email=employee.email)
    except EmployeeBISP.DoesNotExist:
        messages.error(request, "Employee record not found.")


    try:
        personalDetails = EmployeePersonalDetails.objects.filter(employee=employee).first()
    except EmployeePersonalDetails.DoesNotExist:
        personalDetails = None

    try:
        primary_contact = EmployeeEmergencyContact.objects.filter(employee=employee, priority=1).first()
    except EmployeeEmergencyContact.DoesNotExist:
        primary_contact = None

    try:
        secondary_contact = EmployeeEmergencyContact.objects.filter(employee=employee, priority=2).first()
    except EmployeeEmergencyContact.DoesNotExist:
        secondary_contact = None

    try:
        bank_details = EmployeeBankDetails.objects.filter(employee=employee).first()
    except EmployeeBankDetails.DoesNotExist:
        bank_details = None

    try:
        Edu = EmployeeEducation.objects.filter(employee=employee).first()
    except EmployeeEducation.DoesNotExist:
        Edu = None

    try:
        PriExperience = EmployeeExperience.objects.filter(employee=employee, priority=1).first()
    except EmployeeExperience.DoesNotExist:
        PriExperience = None

    try:
        SecExperience = EmployeeExperience.objects.filter(employee=employee, priority=2).first()
    except EmployeeExperience.DoesNotExist:
        SecExperience = None

    try:
        Document = EmployeeDocument.objects.filter(employee=employee)
    except EmployeeDocument.DoesNotExist:
        Document = None


    return render(request, 'admin_templates/profile.html', {'employee':employee,'records': records,'projects': projects.distinct(),'tasks': tasks,'employees': [current_employee],'personalDetails':personalDetails,'primary_contact': primary_contact,'secondary_contact':secondary_contact,'bank_details':bank_details,'Edu':Edu,'PriExperience':PriExperience,'SecExperience':SecExperience,'Document':Document,'total_leave':aggregated_leave})


def Forget_pwd(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/forgot-password.html')

def Contact(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/contacts.html')

def Register(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')


    departments = Department.objects.all()
    designations = Designation.objects.select_related('department').all()

    return render(request,'admin_templates/register.html',{
            'departments': departments,
            'designations': designations,
            'employees':EmployeeBISP.objects.filter(status='active')
        })

def Login_page(request):
    return render(request,'admin_templates/login.html')

def Logout(request):
    logout(request)
    request.session.flush()
    return render(request,'admin_templates/login.html')

#Show All inactive Employee
def Emplist_Inactive(request):

    deleted_employees = EmployeeBISP.objects.filter(status='deleted')

    # Get latest history entry for each deleted employee
    Emp = []
    for emp in deleted_employees:
        latest_history = emp.history.order_by('-version').first()
        if latest_history:
            Emp.append(latest_history)

    return render(request, 'admin_templates/Emp_Inactive_List.html', {'Emp': Emp})

#Show Employee history
def Emplist_History(request):
    try:
        Emp=EmployeeBISPHistory.objects.filter(employee__status='active').order_by('-timestamp','-id')
    except EmployeeBISPHistory.DoesNotExist:
        Emp=None

    return render(request,'admin_templates/Emp_Update_List.html',{'Emp':Emp})

def Active_Emp(request,employee_id):
    # Get the specific history entry

    history_entry = get_object_or_404(EmployeeBISPHistory, id=employee_id)

    # Get the corresponding employee
    employee = history_entry.employee

    employee.name = history_entry.name
    employee.nationality = history_entry.nationality
    employee.current_address = history_entry.current_address
    employee.email = history_entry.email
    employee.password = history_entry.password
    employee.date_of_join = history_entry.date_of_join
    employee.work_location = history_entry.work_location
    employee.designation = history_entry.designation
    employee.department = history_entry.department
    employee.role = history_entry.role
    employee.reported_to = history_entry.reported_to
    # Reactivate
    employee.status = 'active'
    employee.save()

    return redirect('Emplist')

#Show Leave List for Team members ID-12
# Show Leave List for Team members (ID-12)
def Leave_list_approved(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    role = request.session.get('role')  # safely fetch role

    if role == 'Manager':
        # Show only leaves submitted by the manager's team
        manager_id = request.session.get('employee_id')
        team_members = EmployeeBISP.objects.filter(reported_to_id=manager_id)
        leave_queryset = Leave.objects.filter(employee__in=team_members).order_by('-id', '-created_at')
    else:
        # Get all leaves from all employees, ordered by apply_date and then ID (newest first)
        leave_queryset = Leave.objects.order_by('-id', '-created_at')

    return render(request, 'leave_templates/Leave_list_approved.html', {'leave_queryset': leave_queryset})

#ID -12
# def update_leave_approve(request, leave_id):
#     if not request.session.get('employee_id'):
#         return redirect('Login_user_page')
#     leave = get_object_or_404(Leave, id=leave_id)
#     employee = leave.employee  # Get the employee related to this leave
#     leave_days = leave.leave_days  # Get the number of days the leave spans
#
#     if request.method == 'POST':
#         status = request.POST.get('status')
#         rejection_reason = request.POST.get('rejection_reason', None)
#
#         # Update the leave status
#         leave.status = status
#
#         # Handle rejection reason if the status is 'Rejected'
#         if status == 'Rejected' and rejection_reason:
#             employee.availed_leave = max(0, employee.availed_leave - leave_days)
#             employee.remaining_leave = min(employee.total_leave, employee.remaining_leave + leave_days)
#             employee.save()
#             leave.reject_reason = rejection_reason
#             leave.reject_date = timezone.now()
#
#         # Handle when leave is approved
#         elif status == 'Approved':
#             if leave.start_date >= timezone.now().date():  # Ensure the leave date is in the past or today
#                 # Adjust the employee's leave balance
#                 employee.availed_leave = max(0, employee.availed_leave + leave_days)
#                 employee.remaining_leave = max(0, employee.remaining_leave - leave_days)
#
#         # Save the updated leave record
#         leave.save()
#
#         # Save the updated employee record
#         employee.save()
#
#         # Show a success message
#         messages.success(request, f"Leave status updated to {status}.")
#
#         # Redirect after the update
#         return redirect('LeavelistApproved')
#
#     # In case of GET or invalid status, return to leave list or a relevant page
#     return redirect('LeavelistApproved')
#

def update_leave_approve(request, leave_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    employee_id = request.session.get('employee_id')
    try:
        employeeC = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        employeeC=None

    leave = get_object_or_404(Leave, id=leave_id)
    employee = leave.employee  # Get the employee related to this leave
    leave_days = leave.leave_days  # Get the number of days the leave spans
    leave_type = leave.leave_type  # Get the leave type related to this leave
    leave_type_instance = get_object_or_404(LeaveType, name=leave_type)  # Fetch the leave type instance

    if request.method == 'POST':
        status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', None)

        # Update the leave status
        leave.status = status
        leave.approved_by=employeeC


        # Handle rejection reason if the status is 'Rejected'
        if status == 'Rejected' and rejection_reason:
            # Revert leave balance in EmpLeaveType model if rejected
            emp_leave_type_instance = EmpLeaveType.objects.get(employee=employee, leave_type=leave_type_instance)

            emp_leave_type_instance.remaining_leave = min(emp_leave_type_instance.total_leave,
                                                          emp_leave_type_instance.remaining_leave + leave_days)
            emp_leave_type_instance.availed_leave = max(0, emp_leave_type_instance.availed_leave - leave_days)
            emp_leave_type_instance.save()

            leave.reject_reason = rejection_reason
            leave.reject_date = timezone.now()

        # Handle when leave is approved
        elif status == 'Approved':
            if leave.start_date >= timezone.now().date():# Ensure the leave date is in the future or today
                if leave.compensatory_off == 0 :
                    emp_leave_type_instance = EmpLeaveType.objects.get(employee=employee,
                                                                       leave_type=leave_type_instance)
                    emp_leave_type_instance.availed_leave = max(0, emp_leave_type_instance.availed_leave + leave_days)
                    emp_leave_type_instance.remaining_leave = max(0,
                                                                  emp_leave_type_instance.remaining_leave - leave_days)
                    emp_leave_type_instance.save()
                elif leave.compensatory_off == 1:
                    pass

        # Save the updated leave record
        leave.save()

        # Show a success message
        messages.success(request, f"Leave status updated to {status}.")

        # Redirect after the update
        return redirect('LeavelistApproved')

    # In case of GET or invalid status, return to leave list or a relevant page
    return redirect('LeavelistApproved')

#For Administrator Leave Request Approval
def update_leave_approve_dashboard(request, leave_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    employee_id = request.session.get('employee_id')

    try:
        employeeC = EmployeeBISP.objects.get(id=employee_id)
    except EmployeeBISP.DoesNotExist:
        employeeC=None

    leave = get_object_or_404(Leave, id=leave_id)
    employee = leave.employee  # Get the employee related to this leave
    leave_days = leave.leave_days  # Get the number of days the leave spans
    leave_type = leave.leave_type  # Get the leave type related to this leave
    leave_type_instance = get_object_or_404(LeaveType, name=leave_type)  # Fetch the leave type instance

    if request.method == 'POST':
        status = request.POST.get('status')
        rejection_reason = request.POST.get('rejection_reason', None)

        # Update the leave status
        leave.status = status
        leave.approved_by=employeeC


        # Handle rejection reason if the status is 'Rejected'
        if status == 'Rejected' and rejection_reason:
            # Revert leave balance in EmpLeaveType model if rejected
            emp_leave_type_instance = EmpLeaveType.objects.get(employee=employee, leave_type=leave_type_instance)

            emp_leave_type_instance.remaining_leave = min(emp_leave_type_instance.total_leave,
                                                          emp_leave_type_instance.remaining_leave + leave_days)
            emp_leave_type_instance.availed_leave = max(0, emp_leave_type_instance.availed_leave - leave_days)
            emp_leave_type_instance.save()

            leave.reject_reason = rejection_reason
            leave.reject_date = timezone.now()

        # Handle when leave is approved
        elif status == 'Approved':
            if leave.start_date >= timezone.now().date():# Ensure the leave date is in the future or today
                if leave.compensatory_off == 0 :
                    emp_leave_type_instance = EmpLeaveType.objects.get(employee=employee,
                                                                       leave_type=leave_type_instance)
                    emp_leave_type_instance.availed_leave = max(0, emp_leave_type_instance.availed_leave + leave_days)
                    emp_leave_type_instance.remaining_leave = max(0,
                                                                  emp_leave_type_instance.remaining_leave - leave_days)
                    emp_leave_type_instance.save()
                elif leave.compensatory_off == 1:
                    pass

        # Save the updated leave record
        leave.save()

        # Redirect after the update
        return redirect('Hrpanel')

    # In case of GET or invalid status, return to leave list or a relevant page
    return redirect('LeavelistApproved')

def handdbook(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    pdfs = HandbookPDF.objects.all().order_by('-uploaded_at')
    context = {
        'pdf_list': [
            {
                'file_name': pdf.file.name.split('/')[-1],
                'file_url': pdf.file.url,
                'uploaded_at': pdf.uploaded_at,
                'is_active': pdf.is_active,
                'id': pdf.id
            } for pdf in pdfs
        ]
    }
    return render(request,'admin_templates/Handbook.html',context)

def handbook_report(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    latest_pdf = HandbookPDF.objects.filter(is_active=True).order_by('-uploaded_at').first()
    employees = EmployeeBISP.objects.filter(status='active')

    if latest_pdf:
        ack_ids = HandbookAcknowledgement.objects.filter(pdf=latest_pdf).values_list('employee_id', flat=True)
    else:
        ack_ids = []

    return render(request, 'admin_templates/Handbook_Report.html', {
        'employees': employees,
        'acknowledged_ids': ack_ids,
    })


def handbook_Indivi_report(request, pdf_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    pdf = HandbookPDF.objects.get(id=pdf_id)
    acknowledgements = HandbookAcknowledgement.objects.filter(pdf=pdf).select_related('employee')

    return render(request, 'admin_templates/Handbook_Report.html', {
        'pdf': pdf,
        'acknowledgements': acknowledgements,
    })

def handbook_employee(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, email=request.user.email)
    latest_pdf = HandbookPDF.objects.filter(is_active=True).order_by('-uploaded_at').first()

    acknowledgement = None
    if latest_pdf:
        acknowledgement = HandbookAcknowledgement.objects.filter(
            employee=employee,
            pdf=latest_pdf
        ).first()

    return render(request, "admin_templates/Handbook_Employee.html", {
        "employee": employee,
        "latest_pdf": latest_pdf,
        "acknowledgement": acknowledgement,
    })


def Leave_Type_Add(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    departments = Department.objects.all()
    employees = EmployeeBISP.objects.all()
    return render(request,'leave_templates/Leave_Type_Add.html', {
        'departments': departments,
        'employees': employees,
    })

#For Changing Status
def change_leave_status(request, id, status):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    leave_type = get_object_or_404(LeaveType, id=id)

    # Hidden and Delete is not used
    if status in ['active', 'inactive', 'hidden', 'delete']:
            leave_type.status = status
            leave_type.save()

    return redirect('LeaveDetail')  # Replace with your actual view name

#For Leave Detail view
def leave_detail_view(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    # Get all leave types
    leave_types = LeaveType.objects.all().order_by('-id')
    employee_leaves = Leave.objects.all()


    # Create a dictionary: {LeaveType: [Leave, Leave, ...]}
    leaves_by_type = {}

    for leave_type in leave_types:
        employee_leaves = Leave.objects.filter(leave_type=leave_type).select_related('employee').order_by('-created_at')
        leaves_by_type[leave_type] = employee_leaves

        # Paginate the results
    paginator = Paginator(employee_leaves, 8)  # Show 8 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'leaves_by_type': leaves_by_type,
        'page_obj': page_obj
    }
    return render(request, 'leave_templates/Leave_detail_view.html', context)

@csrf_exempt
def add_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        department_name = data.get('name')
        if department_name:
            department = Department.objects.create(name=department_name)
            return JsonResponse({'status': 'success', 'department_id': department.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid department name'})

# View to add a new designation
@csrf_exempt
def add_designation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        department_id = data.get('department_id')
        if title and department_id:
            department = Department.objects.get(id=department_id)
            designation = Designation.objects.create(title=title, department=department)
            return JsonResponse({'status': 'success', 'designation_id': designation.id})
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid data'})

def EmpList(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employees = EmployeeBISP.objects.filter(status='active').all
    return render(request,'admin_templates/Employee_List.html',{'employees': employees})

#For Delete Employee with ID
def delete_employee(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    try:

       employee = get_object_or_404(EmployeeBISP, id=id)
    except EmployeeBISP.DoesNotExist:
        employee=None

    EmployeeBISPHistory.objects.create(
        employee=employee,
        name=employee.name,
        dob=employee.dob,
        gender=employee.gender,
        nationality=employee.nationality,
        permanent_address=employee.permanent_address,
        current_address=employee.current_address,
        phone_number=employee.phone_number,
        email=employee.email,
        password=employee.password,
        aadhar_card=employee.aadhar_card,
        date_of_join=employee.date_of_join,
        work_location=employee.work_location,
        designation=employee.designation,
        department=employee.department,
        role=employee.role,
        profile_picture=employee.profile_picture,
        version=employee.version,
        reported_to=employee.reported_to,
        created_at=employee.timestamp,

    )

    # Save current state to history and soft delete
    employee.soft_delete()

    return redirect('Emplist')


#For Rendering Register.html Page
def update_emp_page(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, id=id)
    departments = Department.objects.all()
    designations = Designation.objects.select_related('department').all()
    return render(request,'admin_templates/register.html', {'employee': employee,'departments': departments,
            'designations': designations,
     'employees': EmployeeBISP.objects.filter(status='active')
})

#For Update Employee with ID
def update_employee(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, id=id)
    if request.method == 'POST':

        # Before updating the employee, save the previous record to the history table
        EmployeeBISPHistory.objects.create(
            employee=employee,
            name=employee.name,
            dob=employee.dob,
            gender=employee.gender,
            nationality=employee.nationality,
            permanent_address=employee.permanent_address,
            current_address=employee.current_address,
            phone_number=employee.phone_number,
            email=employee.email,
            password=employee.password,
            aadhar_card=employee.aadhar_card,
            date_of_join=employee.date_of_join,
            work_location=employee.work_location,
            designation=employee.designation,
            department=employee.department,
            role=employee.role,
            profile_picture=employee.profile_picture,
            version=employee.version,
            reported_to=employee.reported_to,
            created_at=employee.timestamp,

        )

        errors = {}

        # Get form data
        name = request.POST.get('Full_Name', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('PWD', '').strip()
        confirm_password = request.POST.get('RPWD', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        cur_address = request.POST.get('Cur_Address', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()

        reported_to_id = request.POST.get("Reported_To", '').strip()
        reported_to = None
        if reported_to_id:
            try:
                reported_to = EmployeeBISP.objects.get(id=reported_to_id)
            except EmployeeBISP.DoesNotExist:
                errors["Reported_To"] = "Invalid manager selected."


        # Validate required fields
        required_fields = {
            "Full_Name": name, "PWD": password, "RPWD": confirm_password,
             "Role": role,
             "workloc": workloc,
        }

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ')} is required."

        # Validate Name (Only letters)
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors["Full_Name"] = "Name should contain only letters."

        # Validate Role
        if not role:
            errors["role"]=f"Role is required"

        # Validate Email
        if not email:
                errors.setdefault("Email", []).append("Email is required.")
        else:
            try:
                email = email.lower()
                validate_email(email)
            except ValidationError:
                errors.setdefault("Email", []).append("Invalid email format.")

        # Validate password confirmation if provided
        if password and password != confirm_password:
            errors["RPWD"] = "Passwords do not match."


        # Validate Aadhar card number (12 digits)
        # if aadhar and (not aadhar.isdigit() or len(aadhar) != 12):
        #     errors["Aadhar"] = "Aadhar number must be exactly 12 digits."

        # Validate Phone Number (10 digits)
        # if phone and (not phone.isdigit() or len(phone) != 10):
        #     errors["Phone"] = "Phone number must be exactly 10 digits."

        # Validate Date of Joining (DOJ)
        if not doj:
            errors.setdefault("DOJ", []).append("DOJ is required.")
        else:
            try:
                today = datetime.today()
                doj_date = datetime.strptime(doj, "%Y-%m-%d").date()
                if doj_date.year < today.year:
                    errors["DOJ"] = "Date of Joining cannot be from a previous year."
            except ValueError:
                errors["DOJ"] = "Invalid Date of Joining format. Use YYYY-MM-DD."

        # Validate Date of Birth (DOB)
        # if not dob:
        #     errors.setdefault("DOB", []).append("DOB is required.")
        # else:
        #     try:
        #         dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        #         min_dob = datetime(1980, 1, 1).date()  # Set minimum DOB as January 1, 1980
        #         if dob_date < min_dob:
        #             errors["DOB"] = "Date of Birth must be on or after January 1, 1980"
        #         elif dob_date > datetime.now().date():
        #             errors["DOB"] = "Date of Birth must be less than present date"
        #     except ValueError:
        #         errors["DOB"] = "Invalid Date of Birth format. Use YYYY-MM-DD."


        # Validate Department
        if not department:
            errors.setdefault("Department", []).append("Department is required.")
        else:
            try:
                department_obj, created = Department.objects.get_or_create(name=department)
            except Exception as e:
                errors["Department"] = "Invalid department selected."

        # Validate Designation
        if not designation:
            errors.setdefault("Designation", []).append("Designation is required.")
        else:
            # Only proceed with DB interaction if input is valid
            try:
                designation_obj, created = Designation.objects.get_or_create(title=designation,
                                                                             department=department_obj)
            except Exception as e:
                errors["Designation"] =f"{department} has no designation titled '{designation}'."



        # If there are validation errors, return the error response
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)
        print("DOne")
        # If no errors, update the employee data
        employee.name = name
        employee.email = email
        employee.nationality = nationality
        employee.designation = designation_obj
        employee.department = department_obj
        employee.current_address = cur_address
        employee.date_of_join = doj
        employee.work_location = workloc
        employee.role = role
        employee.reported_to=reported_to
        # Save the updated employee data
        employee.save()  # This will increment the version and update the timestamp

        return JsonResponse({"status": "success", "message": "Employee updated successfully!"})

    return render(request, 'admin_templates/register.html', {'employee': employee})




# Password validation function
def validate_password(password):
    # Check for minimum length
    if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return "Password must be at least 8 characters long, at least one uppercase letter, one lowercase letter,one digit and one special character ."

    return None  # If the password is valid


# Validation function for profile image size and extension
def validate_profile_picture(profile_img):
    if profile_img:
        # File extension check
        ext = os.path.splitext(profile_img.name)[1].lower()
        allowed_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in allowed_extensions:
            return "Profile picture must be a .jpg or .png file."

        # File size check (2 MB max)
        max_size = 2 * 1024 * 1024  # 20 MB
        if profile_img.size > max_size:
            return "Profile picture size must be less than 2 MB."

    return None

#Add new Employee
def register_user(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get('Full_Name', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('PWD', '').strip()
        confirm_password = request.POST.get('RPWD', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        cur_address = request.POST.get('Cur_Address', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()



        errors = {}

        reported_to_id = request.POST.get("Reported_To", '').strip()
        reported_to = None
        if reported_to_id:
            try:
                reported_to = EmployeeBISP.objects.get(id=reported_to_id)
            except EmployeeBISP.DoesNotExist:
                errors["Reported_To"] = "Invalid manager selected."

        # Validate required fields
        required_fields = {
            "Full_Name": name, "PWD": password, "RPWD": confirm_password,
             "Role": role,"Cur_Address": cur_address,
             "workloc": workloc,
        }
        # "Per_Address": per_address,"Cur_Address": cur_address Add in Profile

        for field, value in required_fields.items():
            if not value:
                errors[field] = f"{field.replace('_', ' ')} is required."

        # Validate Name (Only letters)
        if name and not re.match(r'^[A-Za-z\s]+$', name):
            errors["Full_Name"] = "Name should contain only letters."

        # Validate Role (check if valid)
        if not role:
            errors["role"] = "Role is required."

        # Validate Email
        if not email:
            errors.setdefault("Email", []).append("Email is required.")
        else:
            try:
                email = email.lower()
                validate_email(email)

                # Check email domain
                allowed_domains = ['gmail.com', 'yahoo.com']
                domain = email.split('@')[-1]
                if domain not in allowed_domains:
                    errors.setdefault("Email", []).append("Only Gmail and Yahoo email addresses are allowed.")

                # Check if email is already in use
                if User.objects.filter(email=email).exists():  # Assuming User is the model you're using
                    errors.setdefault("Email", []).append("This email address is already in use.")

            except ValidationError:
                errors.setdefault("Email", []).append("Invalid email format.")

        # Validate Password Confirmation
        if password != confirm_password:
            errors["RPWD"] = "Passwords do not match."

        # Validate password strength
        password_error = validate_password(password)
        if password_error:
            errors["PWD"] = password_error

        # Validate Aadhar
        # if aadhar and (not aadhar.isdigit() or len(aadhar) != 12):
        #     errors["Aadhar"] = "Aadhar number must be exactly 12 digits."

        # Validate Phone Number
        # if phone and (not phone.isdigit() or len(phone) != 10):
        #     errors["Phone"] = "Phone number must be exactly 10 digits."

        # Validate Date of Joining (DOJ)
        if not doj:
            errors.setdefault("DOJ", []).append("DOJ is required.")
        else:
            try:
                today = datetime.today()
                doj_date = datetime.strptime(doj, "%Y-%m-%d").date()
                four_months_future = (datetime.today() + timedelta(days=120)).date()
                if doj_date.year < today.year:
                    errors["DOJ"] = "Date of Joining cannot be from a previous year."
                elif doj_date > four_months_future:
                    errors["DOJ"] = "Date of Joining cannot be more than 4 months from today."
            except ValueError:
                errors["DOJ"] = "Invalid Date of Joining format. Use YYYY-MM-DD."

        # Validate Date of Birth (DOB) for profile
        # if not dob:
        #     errors.setdefault("DOB", []).append("DOB is required.")
        # else:
        #     try:
        #         dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
        #         min_dob = datetime(1980, 1, 1).date()
        #         if dob_date < min_dob:
        #             errors["DOB"] = "Date of Birth must be on or after January 1, 1980"
        #         elif dob_date > datetime.now().date():
        #             errors["DOB"] = "Date of Birth must be less than present date"
        #     except ValueError:
        #         errors["DOB"] = "Invalid Date of Birth format. Use YYYY-MM-DD."

        # Validate Department and Designation
        if not department:
            errors.setdefault("Department", []).append("Department is required.")
        else:
            try:
                department_obj, created = Department.objects.get_or_create(name=department)
            except Exception:
                errors["Department"] = f"{department} does not exist."

        if not designation:
            errors.setdefault("Designation", []).append("Designation is required.")
        else:
            try:
                designation_obj, created = Designation.objects.get_or_create(title=designation,
                                                                             department=department_obj)
            except Exception:
                errors["Designation"] = f"Designation '{designation}' does not exist in department '{department}'."

        # # Validate profile picture format and size
        # error_message = validate_profile_picture(profile_img)
        # if error_message:
        #     errors["image"] = error_message

        # Return errors if any
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Hash password before saving
        hashed_password = make_password(password)

        # Save employee data
        employee = EmployeeBISP(
            name=name,
            email=email,
            password=hashed_password,
            nationality=nationality,
            current_address=cur_address,
            designation=designation_obj,
            date_of_join=doj,
            work_location=workloc,
            department=department_obj,
            role=role,
            reported_to=reported_to
        )
        employee.save()

        return JsonResponse({"status": "success", "message": "Employee registered successfully!"})

    return render(request, 'admin_templates/register.html')

def show_login_page(request):
    # Check if session already active
    role = request.session.get('role')

    if role == "Administrator":
        return redirect('/Hrpanel')
    elif role == "Employee":
        return redirect('/Emppanel')
    elif role == "Manager":
        return redirect('/Adminpanel')

    # If no session, show login page
    return render(request, 'admin_templates/login.html')

#For Login
@csrf_protect
def Login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    email = request.POST.get("Email", "").strip()
    password = request.POST.get("PWD", "").strip()

    errors = {}
    if not email:
        errors["email_error"] = "Email is required."
    if not password:
        errors["password_error"] = "Password is required."
    if errors:
        return JsonResponse(errors, status=400)

    user = EmployeeBISP.objects.filter(email=email,status='active').first()
    if not user:
        return JsonResponse({"email_error": "No account found with this email."}, status=401)

    if not check_password(password, user.password):
        return JsonResponse({"password_error": "Incorrect password."}, status=401)

    #Fake Django User Login
    # Create a dummy Django user (or link with one if you already do)
    django_user, created = User.objects.get_or_create(username=user.email, email=user.email)
    login(request, django_user)

    # Extend session expiry (set persistent session)
    request.session.set_expiry(60 * 60 * 24 * 30)  # 30 days

    # Set common session data
    request.session['employee_id'] = user.id
    request.session['employee_name'] = user.name
    request.session['email']=user.email
    request.session['role']=user.role
    request.session['designation'] = user.designation.title

    request.session['Currenttime'] =datetime.today().date().isoformat()

    try:
        request.session['ProfileImage'] = user.profile_picture.url
    except Exception:
        request.session['ProfileImage'] = ""  # Fallback if no profile image is available

    # Determine redirect URL based on the user's designation
    if user.role == "Administrator":
        redirect_url = "/Hrpanel"
    elif user.role == "Employee" :
        redirect_url = "/Emppanel"
    elif user.role== "Manager":
        redirect_url = "/Adminpanel"
    else:
        return JsonResponse({"error": "Unauthorized role"}, status=403)

    return JsonResponse({"redirect_url": redirect_url}, status=200)

def generate_random_password(length=8):
    """Generate a random password of given length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

#for Forgot Password
def Forget_passord(request):
    if request.method == "POST":
        email = request.POST.get("Email")
        user = EmployeeBISP.objects.filter(email=email).first()


        if user:

            # Generate a new simple password
            new_password = generate_random_password()
            user.password = make_password(new_password)  # Hash the new password
            user.save()
            # Logic to send a password reset email (Django's built-in system can be used)
            send_mail(
                "Password Reset Request",
                f"your password is {new_password}.",
                "noreply@example.com",
                [email],
                fail_silently=False,
            )
            messages.success(request, "A password reset email has been sent.")
        else:
            messages.error(request, "No account found with this email.")

        return redirect("Forget_password")  # Redirect to the same page

    return render(request, "admin_templates/forgot-password.html")



# =======================================================================================================
def leave_Add_page(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    employee_id = request.session['employee_id']
    employee = EmployeeBISP.objects.filter(id=employee_id).first()

    emp_leave_list = []

    from datetime import datetime, timedelta, date

    if employee:
        joining_date = employee.date_of_join

        # If joining_date is a string, convert it to a date object
        if isinstance(joining_date, str):
            joining_date = datetime.strptime(joining_date, '%Y-%m-%d').date()

        today = date.today()

        def is_effective(leave_type):
            if leave_type.effective_after is None:
                return True

            if leave_type.effective_after_value == 'Year':
                days_to_add = leave_type.effective_after * 365
            elif leave_type.effective_after_value == 'Month':
                days_to_add = leave_type.effective_after * 30
            elif leave_type.effective_after_value == 'Day':
                days_to_add = leave_type.effective_after
            else:
                return True  # fallback

            effective_date = joining_date + timedelta(days=days_to_add)
            return today >= effective_date

        # Assigned leave types
        emp_leaves = EmpLeaveType.objects.select_related('leave_type').filter(
            employee=employee,
            leave_type__status='active',

        )

        for e in emp_leaves:
            if is_effective(e.leave_type):
                emp_leave_list.append({
                    'id': e.leave_type.id,
                    'name': e.leave_type.name,
                    'total_leave': e.total_leave,
                    'remaining_leave': e.remaining_leave,
                    'availed_leave': e.availed_leave,
                })

        # Global leave types
        assigned_ids = EmpLeaveType.objects.values_list('leave_type_id', flat=True)
        global_leaves = LeaveType.objects.filter(status='active').exclude(id__in=assigned_ids)

        for leave in global_leaves:
            if is_effective(leave):
                emp_leave_list.append({
                    'id': leave.id,
                    'name': leave.name,
                    'total_leave': '-',
                    'remaining_leave': '-',
                    'availed_leave': '-',
                })

    return render(request, 'leave_templates/leave_add.html', {
        'employee': employee,
        'leave_data': emp_leave_list,
    })


def Apply_leave(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    errors = {}
    id = request.session.get('employee_id')
    half_day_name=None
    leave_obj = None

    try:
        employee = EmployeeBISP.objects.get(id=id)
    except EmployeeBISP.DoesNotExist:
        errors["id"] = "Employee not found."

    if errors:
        return JsonResponse({"status": "error", "errors": errors}, status=400)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        leavetype = request.POST.get("leavetype", "").strip()
        applydate = request.POST.get("applydate", "").strip()
        fromdate = request.POST.get("fromdate", "").strip()
        tilldate = request.POST.get("tilldate", "").strip()
        reason = request.POST.get("reason", "").strip()
        file = request.FILES.get("file")
        half_day = request.POST.get("halfday") == "on"
        comp_off = request.POST.get("compensatory_off") == "on"
        comp_off_reason = request.POST.get("compensatory_reason", "").strip()
        print(f"Received leave type: '{leavetype}'")

        if not leavetype:
            errors["leavetype"] = "Please select a leave type."
        else:
            try:
                leave_obj = LeaveType.objects.get(name=leavetype)
            except LeaveType.DoesNotExist:
                errors["leavetype"] = "Invalid leave type selected."

        from_date, till_date = None, None

        if not fromdate or not tilldate:
            errors["date"] = "Both start and end dates are required."
        else:
            try:
                from_date = datetime.strptime(fromdate, "%Y-%m-%d").date()
                till_date = datetime.strptime(tilldate, "%Y-%m-%d").date()
                today = timezone.now().date()


                if from_date > till_date:
                    errors["fromdate"] = "Start date cannot be after end date."

                if till_date < today and from_date < today:
                    errors["date"] = f"end date cannot be before today ({today.strftime('%d-%m-%Y')})."

                if from_date < today:
                    errors["fromdate"] = f"Start date cannot be before today ({today.strftime('%d-%m-%Y')})."



            except ValueError:
                errors["date"] = "Invalid date format. Use YYYY-MM-DD."

        if not reason:
            errors["reason"] = "Reason is required."

        # Proceed with the rest of the logic only if leave_obj is valid
        if leave_obj:
            leave_days = 0
            half_day_choices = {}
            half_day_name_parts = []  # Collect half-day descriptions

            if from_date and till_date:
                dates = []
                current = from_date
                while current <= till_date:
                    dates.append(current)
                    current += timedelta(days=1)

                for i, date in enumerate(dates):
                    key = f"halfday_option_{date}"
                    choice = request.POST.get(key)

                    is_sunday = date.weekday() == 6
                    is_holiday = False  # Add your real holiday logic here

                    # Always count weekday
                    if not is_sunday and not is_holiday:
                        if choice in ["first_half", "second_half"]:
                            leave_days += 0.5
                            half_day_choices[str(date)] = choice
                            day_name = date.strftime("%A")
                            formatted_half = choice.replace('_', ' ').title()  # "First Half"
                            half_day_name_parts.append(f"{formatted_half} on {day_name} ({date})")

                        else:
                            leave_days += 1

                    # Sunday/holiday logic — count only if sandwiched
                    elif i > 0 and i < len(dates) - 1:
                        prev = dates[i - 1]
                        next = dates[i + 1]
                        prev_leave = request.POST.get(f"halfday_option_{prev}") or (prev.weekday() != 6)
                        next_leave = request.POST.get(f"halfday_option_{next}") or (next.weekday() != 6)

                        if is_sunday and leave_obj.count_weekends_as_leave and prev_leave and next_leave:
                            leave_days += 1
                        elif is_holiday and leave_obj.count_holidays_as_leave and prev_leave and next_leave:
                            leave_days += 1

                print(f"Total leave days: {leave_days}")
                print("Half-day details:", half_day_choices)

            half_day_name = ", ".join(half_day_name_parts)

            # After leave_obj is fetched and validated
            emp_leave = EmpLeaveType.objects.filter(employee=employee, leave_type=leave_obj).first()
            if not emp_leave:
                errors["leave"] = f"No leave balance found for {leave_obj.name}."
            else:
                remaining_leave = emp_leave.remaining_leave or 0

                print(f"Remaining Leave: {remaining_leave}, Requested: {leave_days}")
                if leave_days > remaining_leave:
                    errors["leave"] = f"Insufficient leave balance! You have {remaining_leave} days left."



        if file:
            allowed_extensions = ["pdf", "jpeg", "jpg", "png"]
            file_extension = file.name.split(".")[-1].lower()
            if file_extension not in allowed_extensions:
                errors["file"] = "Invalid file type. Only PDF, JPEG, JPG, and PNG allowed."
            if file.size > 2 * 1024 * 1024:
                errors["file"] = "File size must be less than 2MB."

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        Leave.objects.create(
            employee=employee,
            leave_type=leave_obj,
            apply_date=applydate,
            start_date=from_date,
            end_date=till_date,
            reason=reason,
            status="Pending",
            attachment=file,
            is_half_day=half_day,
            leave_days = leave_days,
            compensatory_off=comp_off,
            compensatory_reason=comp_off_reason,
            half_day_type_name=half_day_name,

        )

        return JsonResponse({
            "status": "success",
            "message": "Leave application submitted successfully!"
        })


    return render(request, "leave_templates/leave_add.html",{"errors": errors,})



#Show Leave List for particular user
def Leave_list(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    user = request.user  # This is the actual User object
    try:
        # Get the employee record based on the logged-in user's email
        current_employee = EmployeeBISP.objects.prefetch_related(
            Prefetch(
                'leave_set',
                queryset=Leave.objects.all().order_by('-created_at')  # Order newest first
            )
        ).get(email=user.email)
    except EmployeeBISP.DoesNotExist:
        messages.error(request, "Employee record not found.")
        return redirect('applyleave')

    return render(request, 'leave_templates/Leave_list.html', {'employees': [current_employee]})

#Withdraw Leave
def Withdraw_leave(request, leave_id):
    # Fetch the leave record
    leave = get_object_or_404(Leave, id=leave_id)

    # Get leave days and related info
    leave_days = leave.leave_days
    employee = leave.employee
    leave_type = leave.leave_type

    # Get EmpLeaveType record
    emp_leave_type = EmpLeaveType.objects.filter(employee=employee, leave_type=leave_type).first()

    if not emp_leave_type:
        messages.error(request, "Employee leave balance record not found.")
        return redirect('Leavelist')

    # Check if withdrawal is allowed (only if today is same or before leave starts)
    if leave.start_date == datetime.now().date() or datetime.combine(leave.start_date, datetime.min.time()) > datetime.now():
        # Restore leave balances in EmpLeaveType
        emp_leave_type.availed_leave = max(0, emp_leave_type.availed_leave - leave_days)
        emp_leave_type.remaining_leave = min(emp_leave_type.total_leave, emp_leave_type.remaining_leave + leave_days)
        emp_leave_type.save()

        # Update leave status
        leave.status = 'Withdrawn'
        leave.save()

        messages.success(request, f"Leave withdrawn successfully. {leave_days} day(s) added back.")
    elif datetime.now().date() > leave.start_date:
        messages.error(request, "Cannot withdraw leave after its start date.")
    else:
        messages.error(request, "Leave withdrawal failed.")

    return redirect('Leavelist')

def add_leave_type(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    if request.method == 'POST':


        errors = {}

        # Basic info
        leave_name = request.POST.get('leave_name')
        code = request.POST.get('code')
        leave_type = request.POST.get('leave_type')  # Paid / Unpaid

        if not leave_name:
            errors['leave_name'] = "Leave name is required."
        elif LeaveType.objects.filter(name=leave_name).exists():
            errors['leave_name'] = "Leave name is already exists."

        if not code:
            errors['code'] = "Code is required."
        elif LeaveType.objects.filter(code=code).exists():
            errors['code'] = "A leave type with this code already exists."

        if not leave_type:
            errors['leave_type'] = "Leave type is required."

        # Entitlement
        accrual = request.POST.get('accrual') == 'on'
        effective_after = request.POST.get('effective_after') or None
        effective_from = request.POST.get('effective_from') or 'DOJ'
        leave_time = request.POST.get('leave_time') or None
        leave_time_unit = request.POST.get('leave_time_unit')
        leave_frequency = request.POST.get('leave_time_frequency')
        effective_after_unit=request.POST.get('effective_after_unit')

        if not leave_time:
            errors['leave_time']="Leave time is required"

        effective_from = effective_from.upper()
        leave_time_unit = leave_time_unit.upper() if leave_time_unit else None
        leave_frequency = leave_frequency.upper() if leave_frequency else None

        VALID_EFFECTIVE_FROM = ['DOJ', 'CONFIRMATION']
        VALID_UNITS = ['DAYS', 'HOURS']
        VALID_FREQUENCIES = ['MONTHLY', 'YEARLY']

        if effective_from not in VALID_EFFECTIVE_FROM:
            errors['effective_from'] = f"Invalid value '{effective_from}'."
        if leave_time_unit and leave_time_unit not in VALID_UNITS:
            errors['leave_time_unit'] = f"Invalid unit '{leave_time_unit}'."
        if leave_frequency and leave_frequency not in VALID_FREQUENCIES:
            errors['leave_frequency'] = f"Invalid frequency '{leave_frequency}'."

        # Restrictions
        count_weekends_as_leave = request.POST.get('weekend_count') == 'yes'
        count_holidays_as_leave = request.POST.get('holiday_count') == 'yes'

        # Filters
        status = request.POST.get('status', 'active')
        employee_type = request.POST.get('employee_type')  # 'all' or 'individual'
        gender = request.POST.get('gender') if employee_type == 'individual' else None
        marital_status = request.POST.get('marital_status') if employee_type == 'individual' else None

        department = None
        selected_employee = None

        if employee_type == 'individual':
            department_id = request.POST.get('department')
            employee_id = request.POST.get('employee')

            if not gender:
                errors['gender'] = "Gender is required for individual employees."
            if not marital_status:
                errors['marital_status'] = "Marital status is required for individual employees."
            if not department_id:
                errors['department'] = "Department is required."
            else:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    errors['department'] = "Invalid department selected."

            if not employee_id:
                errors['employee'] = "Employee is required."
            else:
                try:
                    selected_employee = EmployeeBISP.objects.get(id=employee_id)
                except EmployeeBISP.DoesNotExist:
                    errors['employee'] = "Invalid employee selected."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            with transaction.atomic():
                # Create LeaveType (as a master/template)
                leave_type_obj = LeaveType.objects.create(
                    name=leave_name,
                    code=code,
                    leave_type=leave_type,
                    accrual=accrual,
                    effective_after=int(effective_after) if effective_after else None,
                    effective_after_value=effective_after_unit,
                    effective_from=effective_from,
                    leave_time=int(leave_time) if leave_time else None,
                    leave_time_unit=leave_time_unit,
                    leave_frequency=leave_frequency,
                    count_weekends_as_leave=count_weekends_as_leave,
                    count_holidays_as_leave=count_holidays_as_leave,
                    status=status,
                    gender=gender,
                    marital_status=marital_status,
                    department=department
                )

                # Assign leave balances to employee(s)
                if leave_time:
                    leave_time = int(leave_time)

                    if employee_type == 'individual' and selected_employee:
                        EmpLeaveType.objects.create(
                            employee=selected_employee,
                            leave_type=leave_type_obj,
                            total_leave=leave_time,
                            remaining_leave=leave_time,
                            availed_leave=0
                        )
                    elif employee_type == 'all':
                        employees = EmployeeBISP.objects.all()
                        EmpLeaveType.objects.bulk_create([
                            EmpLeaveType(
                                employee=emp,
                                leave_type=leave_type_obj,
                                total_leave=leave_time,
                                remaining_leave=leave_time,
                                availed_leave=0
                            ) for emp in employees
                        ])

            return JsonResponse({'status': 'success', 'message': 'Leave Type added successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': {'non_field_error': str(e)}}, status=500)

    return render(request, 'leave_templates/Leave_Type_Add.html')

#For render update leave type page
def update_leave_type_page(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    leave_type = get_object_or_404(LeaveType,id=id)
    departments = Department.objects.all()
    employees = EmployeeBISP.objects.all()
    emp_leave_type = EmpLeaveType.objects.filter(leave_type=leave_type).first()

    return render(request, 'leave_templates/Leave_type_update.html', {'leave_type': leave_type,'emp_lt':emp_leave_type,'departments':departments,'employees':employees})



def update_leave_type(request, leave_type_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    try:
        leave_type = LeaveType.objects.get(id=leave_type_id)
    except LeaveType.DoesNotExist:
        return JsonResponse({'status': 'error', 'errors': {'non_field_error': 'Leave Type not found'}}, status=404)

    if request.method == 'POST':
        errors = {}
        # Save previous state to LeaveTypeHistory
        LeaveTypeHistory.objects.create(
            leave_type=leave_type,
            name=leave_type.name,
            code=leave_type.code,
            accrual=leave_type.accrual,
            effective_after=leave_type.effective_after,
            effective_after_value=leave_type.effective_after_value,
            effective_from=leave_type.effective_from,
            status=leave_type.status,
            leave_time=leave_type.leave_time,
            leave_time_unit=leave_type.leave_time_unit,
            leave_type_field=leave_type.leave_type,
            count_weekends_as_leave=leave_type.count_weekends_as_leave,
            count_holidays_as_leave=leave_type.count_holidays_as_leave,
            leave_frequency=leave_type.leave_frequency,
            gender=leave_type.gender,
            marital_status=leave_type.marital_status,
            department=leave_type.department,
            version=leave_type.version,
            timestamp=leave_type.timestamp,
        )
        leave_type.version += 1  # Increment version

        # Basic info
        leave_name = request.POST.get('leave_name')
        code = request.POST.get('code')
        leave_type_value = request.POST.get('leave_type')  # Paid / Unpaid

        if not leave_name:
            errors['leave_name'] = "Leave name is required."
        if not code:
            errors['code'] = "Code is required."
        elif LeaveType.objects.filter(code=code).exclude(id=leave_type.id).exists():
            errors['code'] = "A leave type with this code already exists."
        if not leave_type_value:
            errors['leave_type'] = "Leave type is required."

        # Entitlement
        accrual = request.POST.get('accrual') == 'on'
        effective_after = request.POST.get('effective_after') or None
        effective_from = request.POST.get('effective_from') or 'DOJ'
        leave_time = request.POST.get('leave_time') or None
        leave_time_unit = request.POST.get('leave_time_unit')
        leave_frequency = request.POST.get('leave_time_frequency')
        effective_after_unit = request.POST.get('effective_after_unit')
        print(effective_after_unit)

        if not leave_time:
            errors['leave_time'] = "Leave time is required"

        effective_from = effective_from.upper()
        leave_time_unit = leave_time_unit.upper() if leave_time_unit else None
        leave_frequency = leave_frequency.upper() if leave_frequency else None

        VALID_EFFECTIVE_FROM = ['DOJ', 'CONFIRMATION']
        VALID_UNITS = ['DAYS', 'HOURS']
        VALID_FREQUENCIES = ['MONTHLY', 'YEARLY']

        if effective_from not in VALID_EFFECTIVE_FROM:
            errors['effective_from'] = f"Invalid value '{effective_from}'"
        if leave_time_unit and leave_time_unit not in VALID_UNITS:
            errors['leave_time_unit'] = f"Invalid unit '{leave_time_unit}'"
        if leave_frequency and leave_frequency not in VALID_FREQUENCIES:
            errors['leave_frequency'] = f"Invalid frequency '{leave_frequency}'"

        # Restrictions
        count_weekends_as_leave = request.POST.get('weekend_count') == 'yes'
        count_holidays_as_leave = request.POST.get('holiday_count') == 'yes'

        # Filters
        status = request.POST.get('status', 'active')
        employee_type = request.POST.get('employee_type')  # 'all' or 'individual'
        gender = request.POST.get('gender') if employee_type == 'individual' else None
        marital_status = request.POST.get('marital_status') if employee_type == 'individual' else None

        department = None
        selected_employee = None

        if employee_type == 'individual':
            department_id = request.POST.get('department')
            employee_id = request.POST.get('employee')

            if not gender:
                errors['gender'] = "Gender is required for individual employees."
            if not marital_status:
                errors['marital_status'] = "Marital status is required for individual employees."
            if not department_id:
                errors['department'] = "Department is required."
            else:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    errors['department'] = "Invalid department selected."

            if not employee_id:
                errors['employee'] = "Employee is required."
            else:
                try:
                    selected_employee = EmployeeBISP.objects.get(id=employee_id)
                except EmployeeBISP.DoesNotExist:
                    errors['employee'] = "Invalid employee selected."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors}, status=400)

        try:
            with transaction.atomic():
                # Update LeaveType
                leave_type.name = leave_name
                leave_type.code = code
                leave_type.leave_type = leave_type_value
                leave_type.accrual = accrual
                leave_type.effective_after = int(effective_after) if effective_after else None
                leave_type.effective_after_value=effective_after_unit
                leave_type.effective_from = effective_from
                leave_type.leave_time = int(leave_time) if leave_time else None
                leave_type.leave_time_unit = leave_time_unit
                leave_type.leave_frequency = leave_frequency
                leave_type.count_weekends_as_leave = count_weekends_as_leave
                leave_type.count_holidays_as_leave = count_holidays_as_leave
                leave_type.status = status
                leave_type.gender = gender
                leave_type.marital_status = marital_status
                leave_type.department = department

                # Store old employee type before updating
                existing_emp_links = EmpLeaveType.objects.filter(leave_type=leave_type)
                employee_count = existing_emp_links.count()

                if employee_count == 1:
                    old_employee_type = 'individual'
                elif employee_count > 1:
                    old_employee_type = 'all'
                else:
                    old_employee_type = None


                leave_type.save()

                # Update EmpLeaveType records
                if leave_time:
                    leave_time = int(leave_time)

                    if employee_type == 'individual' and selected_employee:
                        if old_employee_type == 'all':
                            # Changed from all → individual, so delete all
                            EmpLeaveType.objects.filter(leave_type=leave_type).delete()
                        else:
                            # Same type, ensure we delete only the old individual if different
                            EmpLeaveType.objects.filter(leave_type=leave_type).exclude(
                                employee=selected_employee).delete()

                        # Add/update selected individual
                        EmpLeaveType.objects.update_or_create(
                            employee=selected_employee,
                            leave_type=leave_type,
                            defaults={
                                'total_leave': leave_time,
                                'remaining_leave': leave_time,
                                'availed_leave': 0
                            }
                        )

                    elif employee_type == 'all':
                        if old_employee_type == 'individual':
                            # Changed from individual → all, so delete previous individual's record
                            EmpLeaveType.objects.filter(leave_type=leave_type).delete()

                        employees = EmployeeBISP.objects.all()
                        for emp in employees:
                            EmpLeaveType.objects.update_or_create(
                                employee=emp,
                                leave_type=leave_type,
                                defaults={
                                    'total_leave': leave_time,
                                    'remaining_leave': leave_time,
                                    'availed_leave': 0
                                }
                            )

            return JsonResponse({'status': 'success', 'message': 'Leave Type updated successfully.'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': {'non_field_error': str(e)}}, status=500)

    return render(request, 'leave_templates/Leave_Type_Update.html', {'leave_type': leave_type})


#========================================================================================================================+
#For Handbook PDF
def uploadPDF(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    error_msg = None
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        file = request.FILES['pdf_file']

        if file.content_type != 'application/pdf' or not file.name.lower().endswith('.pdf'):
            error_msg = "Only PDF files are allowed."
        else:
            instance = HandbookPDF.objects.create(file=file, is_active=True)
            HandbookPDF.objects.exclude(id=instance.id).update(is_active=False)

    pdfs = HandbookPDF.objects.all().order_by('-uploaded_at')
    context = {
        'pdf_list': [
            {
                'file_name': pdf.file.name.split('/')[-1],
                'file_url': pdf.file.url,
                'uploaded_at': pdf.uploaded_at,
                'is_active': pdf.is_active,
                'id': pdf.id
            } for pdf in pdfs
        ],
        'error_msg': error_msg,
    }
    return render(request, 'admin_templates/Handbook.html', context)


def acknowledge_handbook(request, pdf_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employee = get_object_or_404(EmployeeBISP, email=request.user.email)
    pdf = get_object_or_404(HandbookPDF, id=pdf_id)

    # Update or create acknowledgement for this employee and PDF
    acknowledgement, created = HandbookAcknowledgement.objects.get_or_create(
        employee=employee,
        pdf=pdf,
        defaults={'status': 'Acknowledge'}
    )

    if not created:
        acknowledgement.status = 'Acknowledge'
        acknowledgement.save()

    return redirect('handbookemployee')

#For download handbook report data in excel form
def export_to_excel_handbook(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    # Create an Excel workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Employee Report"

    # Define column headers
    headers = ['#', 'Employee Name', 'Email', 'Role', 'Status']
    ws.append(headers)

    # Get all employees (you can modify this query if you want to filter)
    employees = EmployeeBISP.objects.all()

    # Loop through employees and check acknowledgment status from the HandbookAcknowledgement model
    for idx, employee in enumerate(employees, start=1):
        # Get the acknowledgment status from the HandbookAcknowledgement model
        handbook_acknowledgement = HandbookAcknowledgement.objects.filter(employee=employee).first()

        # Check if the employee has acknowledged the handbook
        if handbook_acknowledgement and handbook_acknowledgement.status == 'Acknowledge':
            status = 'Acknowledged'
        else:
            status = 'Not Acknowledge'

        # Append employee data to Excel sheet
        ws.append([idx, employee.name, employee.email, employee.role, status])

    # Generate the response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=employee_report.csv'

    # Save the workbook into the response
    wb.save(response)
    return response

#Render Learning Video Page
def Learning_video(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    project_videos = LearningVideo.objects.filter(section="Project Management")
    timesheet_videos = LearningVideo.objects.filter(section="Timesheet Management")
    leave_videos = LearningVideo.objects.filter(section="Leave Management")
    context = {
        'project_videos': project_videos,
        'timesheet_videos': timesheet_videos,
        'leave_videos': leave_videos,
        'is_admin': request.session.get('role') == 'Administrator',
    }
    return render(request, 'admin_templates/Learning_Video.html', context)

@csrf_exempt
#For Upload Learning Video
def upload_learning_video(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        section = request.POST.get('section')
        title = request.POST.get('title')
        video = request.FILES.get('video')
        if section and title and video:
            new_video = LearningVideo.objects.create(title=title, section=section, video=video)
            return JsonResponse({
                'success': True,
                'title': new_video.title,
                'video_url': new_video.video.url
            })
    return JsonResponse({'success': False, 'message': 'Upload failed'})


def update_about_me(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    if request.method == 'POST':


        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        phone_number = request.POST.get('phone_number', '').strip()
        dob = request.POST.get('dob', '').strip()
        current_address = request.POST.get('current_address', '').strip()
        gender = request.POST.get('gender', '').strip()
        reporting_manager = request.POST.get('reporting_manager', '').strip()
        profile_img = request.FILES.get("image")

        field_errors = {}

        # Field validations
        if not phone_number:
            field_errors['phone_number'] = "Phone number is required."
        elif not phone_number.isdigit():
            field_errors['phone_number'] = "Phone number must be Integer."
        elif len(phone_number) != 10:
            field_errors['phone_number'] = "Phone number must be exactly 10 digits."

        # Validate profile picture format and size
        error_message = validate_profile_picture(profile_img)
        if error_message:
            field_errors["image"] = error_message

        if not gender:
            field_errors["gender"] = "Gender is required"


        # Validate Date of Birth (DOB) for profile
        if not dob:
            field_errors.setdefault("dob", []).append("DOB is required.")
        else:
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
                min_dob = datetime(1980, 1, 1).date()
                if dob_date < min_dob:
                       field_errors['dob']= "Date of Birth must be on or after January 1, 1980"
                elif dob_date > datetime.now().date():
                     field_errors['dob']= "Date of Birth must be less than present date"
            except ValueError:
                   field_errors['dob'] = "Invalid Date of Birth format. Use YYYY-MM-DD."

        if field_errors:
            return JsonResponse({'status': 'error', 'errors': field_errors})

        # Save valid data
        employee.phone_number = phone_number
        employee.dob = dob
        employee.current_address = current_address
        employee.gender = gender
        employee.reporting_manager = reporting_manager
        employee.profile_picture=profile_img
        employee.save()

        try:
            request.session['ProfileImage'] =employee.profile_picture.url
        except Exception:
            request.session['ProfileImage'] = ""

        print("Done inside")
        return JsonResponse({'status': 'success', 'message': 'About Me updated successfully.'})

def update_personal_info(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        passport = request.POST.get('passport', '').strip()
        passport_number = request.POST.get('passport_number', '').strip()
        tell_number = request.POST.get('phone_number', '').strip()
        religion = request.POST.get('religion', '').strip()
        marital_status = request.POST.get('marital_status', '').strip()

        field_errors = {}

        # Validate passport number: exactly 12 digits
        if not passport_number or not passport_number.strip():
            field_errors['passport_number'] = "Passport number is required."
        elif not passport_number.isdigit():
            field_errors['passport_number'] = "Passport number must contain only digits."
        elif len(passport_number) != 12:
            field_errors['passport_number'] = "Passport number must be exactly 12 digits."

        # Validate phone number: exactly 10 digits and numeric
        if not tell_number or not tell_number.strip():
            field_errors['phone_number'] = "Phone number is required."
        elif not tell_number.isdigit():
            field_errors['phone_number'] = "Phone number must contain only digits."
        elif len(tell_number) != 10:
            field_errors['phone_number'] = "Phone number must be exactly 10 digits."

        if field_errors:
            return JsonResponse({'status': 'error', 'errors': field_errors})

        # Update EmployeePersonalDetails
        personal_details, created = EmployeePersonalDetails.objects.get_or_create(employee=employee)
        personal_details.passport = passport
        personal_details.passport_number = passport_number
        personal_details.Tell_number = tell_number
        personal_details.religion = religion
        personal_details.marital_status = marital_status
        personal_details.save()

    return JsonResponse({'status': 'success', 'message': 'Personal Info updated successfully.'})


def update_emergency_contact(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        primary_name = request.POST.get('primary_contact_name', '').strip()
        primary_phone = request.POST.get('primary_contact_phone', '').strip()
        primary_relationship = request.POST.get('primary_contact_relationship', '').strip()

        secondary_name = request.POST.get('secondary_contact_name', '').strip()
        secondary_phone = request.POST.get('secondary_contact_phone', '').strip()
        secondary_relationship = request.POST.get('secondary_contact_relationship', '').strip()

        field_errors = {}

        # Validate primary contact
        if not primary_name:
            field_errors['primary_contact_name'] = "Primary contact name is required."
        if not primary_phone:
            field_errors['primary_contact_phone'] = "Primary contact phone is required."
        elif not primary_phone.isdigit() or len(primary_phone) != 10:
            field_errors['primary_contact_phone'] = "Phone number must be Integer of 10 digits."

        # Optional: validate secondary if any value provided
        if any([secondary_name, secondary_phone, secondary_relationship]):
            if not secondary_name:
                field_errors['secondary_contact_name'] = "Secondary contact name is required."
            if not secondary_phone:
                field_errors['secondary_contact_phone'] = "Secondary contact phone is required."
            elif not secondary_phone.isdigit() or len(secondary_phone) != 10:
                field_errors['secondary_contact_phone'] = "Phone number must be Integer of 10 digits."

        if field_errors:
            return JsonResponse({'status': 'error', 'errors': field_errors})

        # Save primary contact
        EmployeeEmergencyContact.objects.update_or_create(
            employee=employee, priority=1,
            defaults={
                'name': primary_name,
                'phone_number': primary_phone,
                'relationship': primary_relationship
            }
        )

        # Save secondary contact (if at least one field is provided)
        if any([secondary_name, secondary_phone, secondary_relationship]):
            EmployeeEmergencyContact.objects.update_or_create(
                employee=employee, priority=2,
                defaults={
                    'name': secondary_name,
                    'phone_number': secondary_phone,
                    'relationship': secondary_relationship
                }
            )

        return JsonResponse({'status': 'success', 'message': 'Emergency contacts updated successfully.'})

def update_bank_info(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        account_no = request.POST.get('account_no', '').strip()
        pan_no = request.POST.get('pan_no', '').strip()
        bank_name = request.POST.get('bank_name', '').strip()
        ifsc_code = request.POST.get('ifsc_code', '').strip()

        errors = {}

        if not bank_name:
            errors["bank_name"] = "Bank name is required."
        if not account_no:
            errors["account_no"] = "Account number is required."
        if not ifsc_code:
            errors["ifsc_code"] = "IFSC code is required."
        if not pan_no:
            errors["pan_no"] = "PAN number is required."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors})

        # Save or update bank info
        bank_details, created = EmployeeBankDetails.objects.get_or_create(employee=employee)
        bank_details.bank_name = bank_name
        bank_details.bank_account_no = account_no
        bank_details.ifsc_code = ifsc_code
        bank_details.pan_no = pan_no
        bank_details.save()

        return JsonResponse({'status': 'success', 'message': 'Bank information updated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def update_education(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        college = request.POST.get('college', '').strip()
        branch = request.POST.get('branch', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        end_date = request.POST.get('end_date', '').strip()

        errors = {}

        if not college:
            errors['college'] = "College name is required."
        if not branch:
            errors['branch'] = "Branch is required."
        if not start_date:
            errors['start_date'] = "Start date is required."
        if not end_date:
            errors['end_date'] = "End date is required."

        # Validate date format and logical order only if both dates are provided
        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                if start_date_obj > end_date_obj:
                    errors['start_date'] = "Start date cannot be after end date."
            except ValueError:
                errors['start_date'] = "Invalid date format. Use YYYY-MM-DD."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors})

        # Update or create education details
        education, created = EmployeeEducation.objects.update_or_create(
            employee=employee,
            institution_name=college,
            defaults={
                'branch': branch,
                'start_date': start_date,
                'end_date': end_date,
            }
        )

        return JsonResponse({'status': 'success', 'message': 'Education updated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def update_experience(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)

        # Retrieve data from the form for primary and secondary experience
        primary_company = request.POST.get('primary_company', '').strip()
        primary_position = request.POST.get('primary_position', '').strip()
        primary_start_date = request.POST.get('primary_start_date', '').strip()
        primary_end_date = request.POST.get('primary_end_date', '').strip()

        secondary_company = request.POST.get('secondary_company', '').strip()
        secondary_position = request.POST.get('secondary_position', '').strip()
        secondary_start_date = request.POST.get('secondary_start_date', '').strip()
        secondary_end_date = request.POST.get('secondary_end_date', '').strip()

        field_errors = {}

        # Validate primary experience
        if not primary_company:
            field_errors['primary_company'] = "company is required."
        if not primary_position:
            field_errors['primary_position'] = " position is required."
        if not primary_start_date:
            field_errors['primary_start_date'] = "start date is required."
        if not primary_end_date:
            field_errors['primary_end_date'] = "end date is required."
        else:
            try:
                primary_start_date_obj = datetime.strptime(primary_start_date, '%Y-%m-%d')
                primary_end_date_obj = datetime.strptime(primary_end_date, '%Y-%m-%d')
                if primary_start_date_obj > primary_end_date_obj:
                    field_errors['primary_start_date'] = " start date cannot be after end date."
            except ValueError:
                field_errors['primary_start_date'] = "Invalid date format for experience. Use a valid date."

        # Validate secondary experience (only if any value is provided)
        if any([secondary_company, secondary_position, secondary_start_date, secondary_end_date]):
            if not secondary_company:
                field_errors['secondary_company'] = "company is required."
            if not secondary_position:
                field_errors['secondary_position'] = " position is required."
            if not secondary_start_date:
                field_errors['secondary_start_date'] = " start date is required."
            if not secondary_end_date:
                field_errors['secondary_end_date'] = " end date is required."
            else:
                try:
                    secondary_start_date_obj = datetime.strptime(secondary_start_date, '%Y-%m-%d')
                    secondary_end_date_obj = datetime.strptime(secondary_end_date, '%Y-%m-%d')
                    if secondary_start_date_obj > secondary_end_date_obj:
                        field_errors['secondary_start_date'] = " start date cannot be after end date."
                except ValueError:
                    field_errors['secondary_start_date'] = "Invalid date format for experience. Use a valid date."

        if field_errors:
            return JsonResponse({'status': 'error', 'errors': field_errors})

        # Delete existing experience records for the employee before saving new ones
        EmployeeExperience.objects.filter(employee=employee).delete()

        # Save primary experience
        EmployeeExperience.objects.create(
            employee=employee,
            company_name=primary_company,
            position=primary_position,
            start_date=primary_start_date_obj,
            end_date=primary_end_date_obj,
            priority=1  # Primary
        )

        # Save secondary experience (if any data is provided)
        if any([secondary_company, secondary_position, secondary_start_date, secondary_end_date]):
            EmployeeExperience.objects.create(
                employee=employee,
                company_name=secondary_company,
                position=secondary_position,
                start_date=secondary_start_date_obj,
                end_date=secondary_end_date_obj,
                priority=2  # Secondary
            )

        return JsonResponse({'status': 'success', 'message': 'Experience details updated successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def upload_document(request, employee_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST':
        employee = get_object_or_404(EmployeeBISP, id=employee_id)
        document_file = request.FILES.get('documentFile')

        errors = {}

        if not document_file:
            errors['documentFile'] = "Document file is required."

        # Optional: file type and size checks
        allowed_extensions = ['.pdf', '.docx', '.jpg', '.jpeg', '.png']
        max_size_mb = 5

        if document_file:
            # Check extension
            if not any(document_file.name.lower().endswith(ext) for ext in allowed_extensions):
                errors['documentFile'] = "Invalid file type. Only PDF, DOCX, JPG, and PNG allowed."

            # Check file size
            if document_file.size > max_size_mb * 1024 * 1024:
                errors['documentFile'] = "File size must be under 5MB."

        if errors:
            return JsonResponse({'status': 'error', 'errors': errors})

        # Save document
        EmployeeDocument.objects.create(
            employee=employee,
            name=document_file.name,
            file=document_file
        )

        return JsonResponse({'status': 'success', 'message': 'Document uploaded successfully.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def upload_employees(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('upload_employees')

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)

            skipped_emails = []
            employees = []
            for i, row in enumerate(reader, start=1):
                emp_name = row.get('Name', '').strip()
                email = row.get('Email', '').strip()

                if not emp_name or not email:
                    print(f"Skipping row {i}: Missing name or email -> {row}")
                    continue

                if EmployeeBISP.objects.filter(email=email).exists():
                    skipped_emails.append(email)
                    continue

                plain_password = row.get('Password', '').strip() or None

                try:
                    dept_name = row.get('Department', '').strip()
                    desig_name = row.get('Designation', '').strip()

                    department = Department.objects.get(name__iexact=dept_name) if dept_name else None
                    designation = Designation.objects.get(title__iexact=desig_name,
                                                          department=department) if desig_name and department else None

                except Department.DoesNotExist:
                    print(f"Department '{dept_name}' not found.")
                    department = None
                except Designation.DoesNotExist:
                    print(f"Designation '{desig_name}' not found for department '{dept_name}'.")
                    designation = None

                try:


                    employee = EmployeeBISP(
                        name=emp_name,
                        role=row.get('Role', '').strip() or 'Employee',
                        department=department,
                        designation=designation,
                        password=make_password(plain_password) if plain_password else None,
                        email=email,
                        nationality=row.get('Nationality', '').strip() or None,
                        current_address=row.get('Current Address', '').strip() or None,
                        date_of_join=row.get('Date Of Joining', '').strip() or None,
                        work_location=row.get('Work Location', '').strip() or None,


                    )
                    employees.append(employee)
                except Exception as e:
                    print(f"Error processing row {i}: {row}")
                    print(f"Exception: {e}")

            print(f"Total valid employees to insert: {len(employees)}")
            if employees:
                try:
                    created = EmployeeBISP.objects.bulk_create(employees)
                    print(f"{len(created)} employees inserted.")
                    messages.success(request, f"{len(created)} employees uploaded successfully.")
                except Exception as e:
                    print("Bulk create error:", e)
                    messages.error(request, f"Database error: {e}")
            else:
                messages.warning(request, "No valid employees found to upload.")

            # Show skipped emails
            if skipped_emails:
                messages.warning(request,f"Skipped {len(skipped_emails)} emails already in use")

        except Exception as e:
            messages.error(request, f"Error processing file: {e}")
            return redirect('upload_employees')

    return render(request, 'admin_templates/register.html')