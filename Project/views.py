import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Project, Task, ProjectHistory, TaskHistory
from HR_App.models import EmployeeBISP
from django.contrib import messages
from django.utils import timezone

# Create your views here.


#For display Add Project Page
def Project_add(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employees = EmployeeBISP.objects.all()

    # Only Admins and Managers
    admin_employees = EmployeeBISP.objects.filter(role__in=["Administrator", "Manager"])

    return render(request,'project_templates/Project_add.html',{'employees': employees,
        'admin_employees': admin_employees})

#For Project Update page
def Project_update_page(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    print(id)
    projects = Project.objects.get(id=id)
    team_member_ids = list(projects.team_members.values_list('id', flat=True))
    employees = EmployeeBISP.objects.all()
    print(team_member_ids)

    # Only Admins and Managers
    admin_employees = EmployeeBISP.objects.filter(role__in=["Administrator", "Manager"])

    return render(request,'project_templates/Project_update.html',{'project':projects,'team_member_ids': team_member_ids,'employees': employees,
        'admin_employees': admin_employees})

def Task_update_page(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    tasks = Task.objects.get(id=id)
    employees = EmployeeBISP.objects.all()
    projects = Project.objects.all()
    return render(request, 'task_templates/Task_update.html',
                  {'task': tasks,'projects':projects,'employees': employees, })


#For Project Update
def update_project(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    project = get_object_or_404(Project, id=id)

    if request.method == "POST":

        history_record = ProjectHistory.objects.create(
            project=project,
            project_name=project.project_name,
            client_name=project.client_name,
            start_date=project.start_date,
            end_date=project.end_date,
            rate_status=project.rate_status,
            rate_currency=project.rate_currency,
            rate_amount=project.rate_amount,
            priority=project.priority,
            leader=project.leader,
            admin=project.admin,
            description=project.description,
            upload_file=project.upload_file,
            version=project.version,
            created_at=project.timestamp,
        )

        # Set ManyToMany team_members after creating the object
        history_record.team_members.set(project.team_members.all())

        errors = {}

        project_name = request.POST.get('project_name')
        client_name = request.POST.get('client_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        rate_status = request.POST.get('rate_status')
        rate_currency = request.POST.get('rate_currency')
        rate_amount = request.POST.get('rate_amount')
        priority = request.POST.get('priority')
        leader_id = request.POST.get('leader')
        admin_id = request.POST.get('admin')
        description = request.POST.get('description')
        team_members = request.POST.getlist('team_members')
        upload_file = request.FILES.get('upload_file')

        # Basic validations
        if not project_name:
            errors['project_name'] = "Project name is required."

        if not client_name:
            errors['client_name'] = "Client name is required."

        if not start_date:
            errors['start_date'] = "Start Date is required."

        if not end_date:
            errors['end_date'] = "End Date is required."

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()

                if start > end:
                    # Assign specific error under end_date instead
                    errors['end_date'] = "End Date cannot be before Start Date."
            except ValueError:
                errors['start_date'] = "Invalid Start Date format."
                errors['end_date'] = "Invalid End Date format."

        if not rate_status:
            errors['rate_status'] = "Rate status is required."

        if not rate_currency:
            errors['rate_currency'] = "Rate currency is required."

        if not priority:
            errors['priority'] = "Priority is required."

        if not description:
            errors['description'] = "Description is required."

        if not team_members:
            errors['team_members'] = "Team Members are required."

        if not rate_amount:
            rate_amount = 0
        try:
            rate_amount = int(rate_amount)
            if rate_amount < 0:
                errors['rate_amount'] = "Rate amount cannot be negative."
        except ValueError:
            errors['rate_amount'] = "Rate amount must be an integer."

        # Check if leader/admin exists
        if not leader_id:
            errors.setdefault("leader", []).append("Leader is required.")
        else:
            if not EmployeeBISP.objects.filter(id=leader_id).exists():
                errors['leader'] = "Selected leader does not exist."

        if not admin_id:
            errors.setdefault("admin", []).append("Admin is required.")
        else:
            if not EmployeeBISP.objects.filter(id=admin_id).exists():
                errors['admin'] = "Selected admin does not exist."

        # Validate file upload
        if upload_file:
            allowed_extensions = ['pdf', 'jpeg', 'jpg', 'png']
            ext = upload_file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                errors['upload_file'] = "Invalid file type. Allowed: PDF, JPEG, JPG, PNG."
            if upload_file.size > 2 * 1024 * 1024:
                errors['upload_file'] = "File must be under 2MB."

        # Return errors if found
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # No validation errors - update project
        project.project_name = project_name
        project.client_name = client_name
        project.start_date = start_date
        project.end_date = end_date
        project.rate_status = rate_status
        project.rate_currency = rate_currency
        project.rate_amount = rate_amount if rate_amount else None
        project.priority = priority
        project.leader_id = leader_id
        project.admin_id = admin_id
        project.description = description

        if upload_file:
            project.upload_file = upload_file

        try:
            project.save()
            project.team_members.set(team_members)
            return JsonResponse({"status": "success", "message": "Project updated successfully!"})
        except Exception as e:
            return JsonResponse({"status": "error", "errors": {"server": str(e)}}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

#For Update Task
def update_task(request, id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    task = get_object_or_404(Task, id=id)
    projects = Project.objects.filter(status='active')
    employees = EmployeeBISP.objects.filter(status='active')

    if request.method == 'POST':
        task_title = request.POST.get('task_title')
        project_id = request.POST.get('project')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status')
        priority = request.POST.get('priority')
        assigned_to_id = request.POST.get('assigned_to')
        description = request.POST.get('description')

        errors = {}

        # Validation
        if not task_title:
            errors['task_title'] = "Task title is required."
        if not project_id:
            errors['project'] = "Project is required."
        if not start_date or not end_date:
            errors['dates'] = "Start and end dates are required."
        if not status:
            errors['status'] = "Status is required."
        if not priority:
            errors['priority'] = "Priority is required."
        if not assigned_to_id:
            errors['assigned_to'] = "Assigned employee is required."
        if not description:
            errors['description'] = "Description is required."

        if not start_date:
            errors['start_date'] = "Start Date is required."

        if not end_date:
            errors['end_date'] = "End Date is required."

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()

                if start > end:
                    # Assign specific error under end_date instead
                    errors['end_date'] = "End Date cannot be before Start Date."
            except ValueError:
                errors['start_date'] = "Invalid Start Date format."
                errors['end_date'] = "Invalid End Date format."

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        # Save current state in history BEFORE changing the task
        TaskHistory.objects.create(
            task=task,
            task_title=task.task_title,
            project=task.project,
            start_date=task.start_date,
            end_date=task.end_date,
            status=task.status,  # This status is business status, not 'active/inactive'
            priority=task.priority,
            assigned_to=task.assigned_to,
            description=task.description,
            version=task.version,
            status_field='active',  # This is historical record's status
            created_at=task.timestamp
        )

        # Update Task
        task.task_title = task_title
        task.project = Project.objects.get(id=project_id)
        task.start_date = start
        task.end_date = end
        task.status = status  # This is the task's working status like "Inprogress"
        task.priority = priority
        task.assigned_to = EmployeeBISP.objects.get(id=assigned_to_id)
        task.description = description
        task.save()  # version auto-increments in the model

        return JsonResponse({'success': True, 'message': 'Task updated successfully.'})

    return render(request, 'tasks/update_task.html', {
        'task': task,
        'projects': projects,
        'employees': employees,
    })

#For Display list of Project
def Project_list(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)

    # Check if the employee is an administrator
    if employee.role == 'Administrator':
        # Admin can see all projects
        projects = Project.objects.filter(status='active').order_by('-created_at')

    elif employee.role == 'Manager':
        # Regular employees can only see projects they lead or are team members of
        projects = Project.objects.filter(leader=employee,status='active').order_by('-created_at') | Project.objects.filter(admin=employee,status='active').order_by('-created_at')
    else:
        projects = Project.objects.filter(team_members =employee,status='active').order_by('-created_at')


    return render(request, 'project_templates/project_list.html', {'projects': projects.distinct()})

#For Task List Display
def Task_list(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    employee_id = request.session.get('employee_id')
    employee = EmployeeBISP.objects.get(id=employee_id)  # Fetch the employee from the database

    # Check if the user is an administrator based on the 'role' field
    if employee.role == 'Administrator':  # Assuming 'Administrator' is the role name in the field
        tasks = Task.objects.filter(project__status='active').order_by('-created_at')  # Show all tasks if user is an admin
    else:
        tasks = Task.objects.filter(assigned_to=employee,project__status='active').exclude(status='Completed').order_by('-created_at')  # Show only tasks assigned to the logged-in user

    return render(request, 'task_templates/Task_list.html', {'tasks': tasks})


#Render Add_task Page
def Task_add_page(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    projects = Project.objects.all()
    employees = EmployeeBISP.objects.all()
    return render(request,'task_templates/Task_add.html', {'projects': projects, 'employees': employees})

#Task Detail
def Task_detail(request,id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    task = get_object_or_404(Task, pk=id)
    task_records = task.records.all()
    paginator = Paginator(task_records, 5)  # Show 5 records per page
    page_number = request.GET.get('page')  # Get the page number from URL
    page_obj = paginator.get_page(page_number)
    context = {
        'task': task,
        'status_choices': Task.STATUS_CHOICES,
        'page_obj': page_obj,
    }
    return render(request,'task_templates/Task_detail.html',context)

#Updating Status of Task
def update_task_status(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')

        try:
            task = Task.objects.get(id=task_id)
            task.status = status
            task.created_at=timezone.now()
            task.save()
            return redirect('Project:task_detail', id=task_id)
        except Task.DoesNotExist:
            return redirect('Project:task_list')  # or handle error better

    return redirect('Project:task_list')

#Adding Task
def add_Task(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    projects = Project.objects.all()
    employees = EmployeeBISP.objects.all()
    errors = {}

    if request.method == 'POST':
        # Get form data
        task_title = request.POST.get('task_title', '').strip()
        project_id = request.POST.get('project')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        status = request.POST.get('status', '').strip()
        priority = request.POST.get('priority', '').strip()
        assigned_to_id = request.POST.get('assigned_to')
        description = request.POST.get('description', '').strip()

        # Basic validations
        if not task_title:
            errors['task_title'] = "Task title is required."

        if not project_id:
            errors['project'] = "Project is required."

        if not start_date:
            errors['start_date'] = "Start Date is required."

        if not end_date:
            errors['end_date'] = "End Date is required."

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()

                if start > end:
                    # Assign specific error under end_date instead
                    errors['end_date'] = "End Date cannot be before Start Date."
            except ValueError:
                errors['start_date'] = "Invalid Start Date format."
                errors['end_date'] = "Invalid End Date format."

        if not status:
            errors['status'] = "Status is required."

        if not priority:
            errors['priority'] = "Priority is required."

        if not description:
            errors['description'] = "Description is required."

        # Check if assigned employee exists
        if not  assigned_to_id :
            errors.setdefault("assigned_to", []).append("Assigned Employee is required.")
        else:
            try:
                assigned_to = EmployeeBISP.objects.get(id=assigned_to_id)
            except EmployeeBISP.DoesNotExist:
                errors['assigned_to'] = "Assigned employee does not exist."

        # If there are any errors, return them
        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Create the task
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            errors['project'] = "Selected project does not exist."
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        task = Task.objects.create(
            task_title=task_title,
            project=project,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,
            assigned_to=assigned_to,
            description=description
        )

        return JsonResponse({"status": "success", "message": "Task added successfully!"})

    return render(request, 'task_templates/Task_add.html', {'projects': projects, 'employees': employees})

#For Add project
def add_project(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    employees = EmployeeBISP.objects.all()
    errors = {}

    if request.method == 'POST':
        project_name = request.POST.get('project_name', '').strip()
        client_name = request.POST.get('client_name', '').strip()
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        rate_status = request.POST.get('rate_status', '').strip()
        rate_currency = request.POST.get('rate_currency', '').strip()
        rate_amount = request.POST.get('rate_amount', '').strip()
        priority = request.POST.get('priority', '').strip()
        leader_id = request.POST.get('leader')
        admin_id = request.POST.get('admin')
        team_members = request.POST.getlist('team_members')
        description = request.POST.get('description', '').strip()
        upload_file = request.FILES.get('upload_file')

        # Basic validations
        if not project_name:
            errors['project_name'] = "Project name is required."

        if not client_name:
            errors['client_name'] = "Client name is required."

        if not start_date:
            errors['start_date'] = "Start Date is required."

        if not end_date:
            errors['end_date'] = "End Date is required."

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d").date()
                end = datetime.strptime(end_date, "%Y-%m-%d").date()

                if start > end:
                    # Assign specific error under end_date instead
                    errors['end_date'] = "End Date cannot be before Start Date."
            except ValueError:
                errors['start_date'] = "Invalid Start Date format."
                errors['end_date'] = "Invalid End Date format."

        if not rate_status:
            errors['rate_status'] = "Rate status is required."

        if not rate_currency:
            errors['rate_currency'] = "Rate currency is required."

        if not priority:
            errors['priority'] = "Priority is required."

        if not description:
            errors['description'] = "Description is required."

        if not team_members:
            errors['team_members'] ="Team Members is required"

        if not rate_amount:
            rate_amount = 0
        try:
            rate_amount = int(rate_amount)
            if rate_amount < 0:
                errors['rate_amount'] = "Rate amount cannot be negative."
        except ValueError:
            errors['rate_amount'] = "Rate amount must be an integer."

        # Validate file upload
        if upload_file:
            allowed_extensions = ['pdf', 'jpeg', 'jpg', 'png']
            ext = upload_file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                errors['upload_file'] = "Invalid file type. Allowed: PDF, JPEG, JPG, PNG."
            elif upload_file.size > 2 * 1024 * 1024:  # 2MB size limit (2 * 1024 * 1024 bytes)
                errors['upload_file'] = "File must be under 2MB."

        # Check if leader/admin exists
        if not leader_id:
            errors.setdefault("leader", []).append("Leader is required.")
        else:
            try:
                leader = EmployeeBISP.objects.get(id=leader_id)
            except EmployeeBISP.DoesNotExist:
                errors['leader'] = "Selected leader does not exist."

        if not admin_id:
            errors.setdefault("admin", []).append("Admin is required.")
        else:
            try:
                admin = EmployeeBISP.objects.get(id=admin_id)
            except EmployeeBISP.DoesNotExist:
                errors['admin'] = "Selected admin does not exist."

        # Validate file upload
        if upload_file:
            allowed_extensions = ['pdf', 'jpeg', 'jpg', 'png']
            ext = upload_file.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                errors['upload_file'] = "Invalid file type. Allowed: PDF, JPEG, JPG, PNG."
            if upload_file.size > 2 * 1024 * 1024:
                errors['upload_file'] = "File must be under 2MB."

        if errors:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

        # Save project
        project = Project.objects.create(
            project_name=project_name,
            client_name=client_name,
            start_date=start_date,
            end_date=end_date,
            rate_status=rate_status,
            rate_currency=rate_currency,
            rate_amount=rate_amount,
            priority=priority,
            leader=leader,
            admin=admin,
            description=description,
            upload_file=upload_file
        )

        project.team_members.set(team_members)
        return JsonResponse({"status": "success", "message": "Project added successfully!"})

    return render(request, 'project_templates/Project_add.html', {'employees': employees})

def project_detail(request, pk):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    project = get_object_or_404(Project, pk=pk)
    task=Task.objects.filter(project=project)
    context = {
        'project': project,
        'task':task
    }
    return render(request, 'project_templates/project_detail.html', context)

def project_history_detail(request, pk):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    project = get_object_or_404(ProjectHistory, pk=pk)

    context = {
        'project': project,

    }
    return render(request, 'project_templates/project_detail.html', context)


#For showing project as completed
def mark_project_completed(request, project_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.soft_delete()
    return redirect('Project:project_list')

#In Adding new Task show assigned employee according to employee
def get_project_employees(request, project_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    if request.method == "GET":
        try:
            project = Project.objects.get(id=project_id)
            team_members = project.team_members.filter(status='active').exclude(role='Administrator')  # adjust field names if needed

            employees_data = [
                {
                    'id': emp.id,
                    'name': emp.name,
                    'designation': emp.designation.title if emp.designation else ''
                }
                for emp in team_members
            ]
            return JsonResponse({'status': 'success', 'employees': employees_data})
        except Project.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Project not found'})

def Project_history(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    try:
        Pro=ProjectHistory.objects.filter(project__status='active').order_by('-timestamp')
    except ProjectHistory.DoesNotExist:
        Pro=None

    return render(request,'project_templates/Project_history.html',{'Pro':Pro})

def Task_history(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    try:
        Task=TaskHistory.objects.filter(task__status_field='active').order_by('-timestamp')
    except TaskHistory.DoesNotExist:
        Task=None

    return render(request,'task_templates/Task_history.html',{'Task':Task})

