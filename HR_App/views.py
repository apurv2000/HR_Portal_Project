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
from django.db.models import Prefetch, Sum, Value, CharField
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, time
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from Project.models import Project,Task
from .models import EmployeeBISP, Leave, LeaveType, Designation, Department, HandbookPDF, \
    HandbookAcknowledgement, EmpLeaveType, EmployeeBISPHistory, LeaveTypeHistory, \
    LearningVideo  # Import your Employee model
from openpyxl import Workbook
from datetime import date, timedelta


# Create your views here.
def Manager(request):
    if request.session.get('role') != "Manager":
        return redirect("Login")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    employee = EmployeeBISP.objects.get(id=employee_id)

    # Get all projects where the employee is admin or leader
    project_qs = Project.objects.filter(admin=employee) | Project.objects.filter(leader=employee)

    # Get related tasks from those projects
    task_qs = Task.objects.filter(assigned_to=employee)


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

    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee':EmployeeBISP.objects.count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,

    }

    return render(request, 'admin_templates/index.html',context)


def Hr(request):
    # Ensure only Administrator can access
    if request.session.get('role') != "Administrator":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")
    employee = EmployeeBISP.objects.get(id=employee_id)

    # Get all projects where the employee is admin or leader
    project_qs = Project.objects.filter(admin=employee) | Project.objects.filter(leader=employee)

    #All Employee leave
    employee_leaves = Leave.objects.filter(status='Pending').order_by('-created_at')[:5]

    # Get related tasks from those projects
    task_qs = Task.objects.filter(assigned_to=employee)

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

    # Annotate and fetch
    latest_tasks = Task.objects.filter(
        assigned_to__isnull=False,
        status='Claimed Completed'
    ).annotate(
        activity_type=Value('Task', output_field=CharField())
    )

    latest_leaves = Leave.objects.filter(employee__isnull=False).annotate(
        activity_type=Value('Leave', output_field=CharField())
    )

    latest_projects = Project.objects.filter(
        team_members__isnull=False
    ).annotate(
        activity_type=Value('Project', output_field=CharField())
    )

    # Attach normalized datetime (prefer updated_at or fallback)
    for item in chain(latest_tasks, latest_leaves, latest_projects):
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
        chain(latest_tasks[:5], latest_leaves[:5], latest_projects[:5]),
        key=lambda x: x.activity_datetime,
        reverse=True
    )[:10]

    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee': EmployeeBISP.objects.count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,
        'employee_leaves': employee_leaves,
        'latest_activities': combined_activities,

    }

    return render(request, 'admin_templates/hr_dashboard.html',context)


def Employee(request):
    if request.session.get('role') != "Employee":
        return redirect("Login_user_page")

    employee_id = request.session.get('employee_id')
    if not employee_id:
        return redirect("Login_user_page")

    employee = EmployeeBISP.objects.get(id=employee_id)

    # Get all projects where the employee is admin or leader
    project_qs = Project.objects.filter(team_members = employee)

    # Get related tasks from those projects
    task_qs = Task.objects.filter(assigned_to=employee)
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
        team_members=employee
    ).annotate(
        activity_type=Value('Project', output_field=CharField())
    )

    # Attach normalized datetime (prefer updated_at or fallback)
    for item in chain(latest_tasks, latest_leaves, latest_projects):
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
        chain(latest_tasks[:5], latest_leaves[:5], latest_projects[:5]),
        key=lambda x: x.activity_datetime,
        reverse=True
    )[:10]

    context = {
        'total_projects': project_qs.count(),
        'total_tasks': task_qs.count(),
        'projects': project_qs,
        'tasks': task_qs,
        'total_employee': EmployeeBISP.objects.count(),
        'status_counts': status_counts,
        'overdue_tasks': overdue_tasks,
        'status_percentages': status_percentages,
        'leave_totals': aggregated_leave,
        'latest_activities': combined_activities,

    }


    return render(request,'admin_templates/Emp_dashboard.html',context)

def Profile(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    return render(request,'admin_templates/profile.html')


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
        })

def Login_page(request):
    return render(request,'admin_templates/login.html')

def Logout(request):
    logout(request)
    request.session.flush()
    return render(request,'admin_templates/login.html')


#Show Leave List for Team members ID-12
def Leave_list_approved(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    # Get all leaves from all employees, ordered by apply_date and then ID (newest first)
    leave_queryset = Leave.objects.order_by('-created_at','-id')  # Most recent application first

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
        employee=None

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
        employee=None

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
    employees = EmployeeBISP.objects.all()

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
    leave_types = LeaveType.objects.all()
    employee_leaves = Leave.objects.all()


    # Create a dictionary: {LeaveType: [Leave, Leave, ...]}
    leaves_by_type = {}

    for leave_type in leave_types:
        employee_leaves = Leave.objects.filter(leave_type=leave_type).select_related('employee')
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

    employee = get_object_or_404(EmployeeBISP, id=id)

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
            'designations': designations,})

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
            timestamp=employee.timestamp,

        )

        errors = {}

        # Get form data
        name = request.POST.get('Full_Name', '').strip()
        email = request.POST.get('Email', '').strip()
        password = request.POST.get('PWD', '').strip()
        confirm_password = request.POST.get('RPWD', '').strip()
        dob = request.POST.get('DOB', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        per_address = request.POST.get('Per_Address', '').strip()
        cur_address = request.POST.get('Cur_Address', '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_img = request.FILES.get("image")
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()


        # Validate required fields
        required_fields = {
            "Full_Name": name, "PWD": password, "RPWD": confirm_password,
             "Role": role,
             "workloc": workloc, "gender": gender
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


        # Validate profile image format
        error_message = validate_profile_picture(profile_img)
        if error_message:
            errors["image"] = error_message

        # If there are validation errors, return the error response
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)
        print("DOne")
        # If no errors, update the employee data
        employee.name = name
        employee.email = email
        employee.dob = dob
        employee.nationality = nationality
        employee.designation = designation_obj
        employee.department = department_obj
        employee.permanent_address = per_address
        employee.current_address = cur_address
        employee.aadhar_card = aadhar
        employee.phone_number = phone
        employee.date_of_join = doj
        employee.work_location = workloc
        employee.gender = gender
        employee.role = role

        # Handle profile image upload if provided
        if profile_img:
            employee.profile_picture = profile_img

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

        # File size check (20 MB max)
        max_size = 20 * 1024 * 1024  # 20 MB
        if profile_img.size > max_size:
            return "Profile picture size must be less than 20 MB."

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
        dob = request.POST.get('DOB', '').strip()
        nationality = request.POST.get('Nationality', '').strip()
        designation = request.POST.get('Designation', '').strip()
        per_address = request.POST.get('Per_Address', '').strip()
        cur_address = request.POST.get('Cur_Address', '').strip()
        aadhar = request.POST.get('Aadhar', '').strip()
        phone = request.POST.get('Phone', '').strip()
        doj = request.POST.get('DOJ', '').strip()
        workloc = request.POST.get('workloc', '').strip()
        gender = request.POST.get('gender', '').strip()
        profile_img = request.FILES.get("image")
        department = request.POST.get("Department", '').strip()
        role = request.POST.get("role", '').strip()

        errors = {}

        # Validate required fields
        required_fields = {
            "Full_Name": name, "PWD": password, "RPWD": confirm_password,
             "Role": role,"Cur_Address": cur_address,
             "workloc": workloc, "gender": gender
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

        # Validate profile picture format and size
        error_message = validate_profile_picture(profile_img)
        if error_message:
            errors["image"] = error_message

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
            dob=dob,
            gender=gender,
            nationality=nationality,
            permanent_address=per_address,
            current_address=cur_address,
            phone_number=phone,
            aadhar_card=aadhar,
            designation=designation_obj,
            date_of_join=doj,
            work_location=workloc,
            department=department_obj,
            profile_picture=profile_img,
            role=role
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

    user = EmployeeBISP.objects.filter(email=email).first()
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

                if from_date > till_date:
                    errors["fromdate"] = "Start date cannot be after end date."

                if from_date < timezone.now().date():
                    errors["limit"] = f"Start date never become before {timezone.now().date().strftime('%d-%m-%Y'):}"
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
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        file = request.FILES['pdf_file']
        instance = HandbookPDF.objects.create(file=file, is_active=True)  # Save model instance
        # You may want to deactivate previous active ones
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
        ]
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