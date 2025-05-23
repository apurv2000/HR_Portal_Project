import os

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import TaskRecord, ImagetaskRecord
from HR_App.models import EmployeeBISP
from Project.models import Task,Project
from datetime import date
from django.views.decorators.csrf import csrf_exempt

# Allowed file extensions
ALLOWED_EXTENSIONS = ['.pdf', '.docx', '.doc', '.jpg', '.jpeg', '.png']
def timesheet_record(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    today = date.today()
    monday_this_week = today - timedelta(days=today.weekday())  # Monday of current week
    monday_last_week = monday_this_week - timedelta(days=7)  # Monday of last week
    sunday_this_week = monday_this_week + timedelta(days=6)  # Sunday of current week

    # Week date list (optional for template display)
    dates = [monday_last_week + timedelta(days=i) for i in range(14)]

    # Get current employee
    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)

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

    return render(request, 'timesheet_templates/timesheet_record.html', {
        'dates': dates,
        'records': records,
    })
#Function for show all employee timesheet record
def timesheet_record_all(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    today = date.today()
    monday_this_week = today - timedelta(days=today.weekday())  # Monday of current week
    monday_last_week = monday_this_week - timedelta(days=7)     # Monday of last week
    sunday_this_week = monday_this_week + timedelta(days=6)     # Sunday of current week

    # Week date list (optional for template display)
    dates = [monday_last_week + timedelta(days=i) for i in range(14)]

    # Filter TaskRecords for both current and previous week
    records = TaskRecord.objects.filter(
        date__range=(monday_last_week, sunday_this_week)
    ).order_by('-id', '-date')

    # Calculate hours
    for record in records:
        if record.start_time and record.end_time:
            start_dt = datetime.combine(record.date, record.start_time)
            end_dt = datetime.combine(record.date, record.end_time)
            duration = end_dt - start_dt
            record.hours = round(duration.total_seconds() / 3600, 2)
        else:
            record.hours = 0

    return render(request, 'timesheet_templates/timesheet_record_all.html', {
        'dates': dates,
        'records': records,
    })
def timesheet_record_image(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')


    # Filter TaskRecords for both current and previous week
    records =ImagetaskRecord.objects.all().order_by('-start_date')


    return render(request, 'timesheet_templates/timesheet_record_image.html', {
        'records': records,
    })

def get_week_dates(last_week=False):

    today = date.today()
    monday = today - timedelta(days=today.weekday())
    if last_week:
        monday -= timedelta(days=7)
    return [monday + timedelta(days=i) for i in range(6)]  # Mon to Sat


def timesheet_add(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    if request.method == "POST":
        errors = {}
        emp_id = request.session['employee_id']
        at_least_one_filled = False  # Track if any valid row is submitted

        def validate_and_create_day_entry(i):
            nonlocal at_least_one_filled
            task_id = request.POST.get(f'task_{i}', '').strip()
            project_id = request.POST.get(f'project_{i}', '').strip()
            date = request.POST.get(f'date_{i}', '').strip()
            start = request.POST.get(f'start_{i}', '').strip()
            end = request.POST.get(f'end_{i}', '').strip()
            desc = request.POST.get(f'description_{i}', '').strip()
            file = request.FILES.get(f'file_{i}')

            day_errors = {}

            # Only validate and save if project is selected
            if project_id or task_id or desc:
                at_least_one_filled = True

                if task_id and (not project_id or not desc):
                    if not project_id:
                        day_errors["project"] = "Project is required "
                    if not desc:
                        day_errors["description"] = "Description is required "

                if desc and (not project_id or not task_id):
                    if not project_id:
                        day_errors["project"] = "Project is required "
                    if not task_id:
                        day_errors["task"] = "Task is required "

                if project_id and (not desc or not task_id):
                    if not desc:
                        day_errors["description"] = "Description is required "
                    if not task_id:
                        day_errors["task"] = "Task is required "


                if not date:
                    day_errors["date"] = "Date is required."
                if not start:
                    day_errors["start"] = "Start time is required."
                if not end:
                    day_errors["end"] = "End time is required."


                # File size check
                if file:
                    if file.size > 2 * 1024 * 1024:
                        day_errors['file'] = "File size must not exceed 2MB."
                    ext = os.path.splitext(file.name)[1].lower()
                    if ext not in ALLOWED_EXTENSIONS:
                        day_errors['file'] = "Invalid file format."

                # Time check
                if start and end:
                    try:
                        start_time = datetime.strptime(start, "%H:%M")
                        end_time = datetime.strptime(end, "%H:%M")
                        if start_time >= end_time:
                            day_errors["start"] = "Start time must be before end time."
                            day_errors["end"] = "End time must be after start time."
                    except ValueError:
                        day_errors["start"] = "Invalid start time format."
                        day_errors["end"] = "Invalid end time format."

                # Save only if no errors
                if not day_errors:
                    try:
                        task = Task.objects.get(id=task_id)
                        TaskRecord.objects.create(
                            task=task,
                            date=date,
                            start_time=start,
                            end_time=end,
                            record_name=desc,
                            attachment=file
                        )
                    except Task.DoesNotExist:
                        day_errors["task"] = "Invalid task selected."
                    except Exception as e:
                        day_errors["error"] = str(e)

            return day_errors

        # Loop through Mon–Sat (1–6)
        for i in range(1, 7):
            day_errors = validate_and_create_day_entry(i)
            if day_errors:
                errors[f'day_{i}'] = day_errors

        # Sunday (if selected)
        if request.POST.get('date_8'):
            day_errors = validate_and_create_day_entry(8)
            if day_errors:
                errors['day_8'] = day_errors

        # No row selected at all
        if not at_least_one_filled:
            return JsonResponse({
                "status": "error",
                "errors": {"general": "Please fill at least one row with project and task details."}
            }, status=400)

        if not errors:
            return JsonResponse({"status": "success", "message": "Timesheet successfully submitted!"})
        else:
            return JsonResponse({"status": "error", "errors": errors}, status=400)

    # GET request – render form
    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)
    last_week = request.GET.get('last_week') == '1'

    # Get week dates
    raw_week_dates = get_week_dates(last_week)

    # Fetch all TaskRecords for that employee and week
    existing_records = TaskRecord.objects.filter(
        task__assigned_to=employee,
        date__in=raw_week_dates
    ).exclude(task__status='Completed').select_related('task', 'task__project')

    # Convert records to a dict: key = date string
    record_map = {}
    for record in existing_records:
        date_str = record.date.strftime('%Y-%m-%d')
        record_map[date_str] = {
            'project': record.task.project.id,
            'task': record.task.id,
            'description': record.record_name,
            'start_time': record.start_time.strftime('%H:%M'),
            'end_time': record.end_time.strftime('%H:%M'),
            'attachment': record.attachment.url if record.attachment else ''
        }

    # Prepare week data but exclude already filled days
    week_data = [
        {'day': d.strftime('%A'), 'date': d.strftime('%Y-%m-%d')}
        for d in raw_week_dates
        if d.strftime('%Y-%m-%d') not in record_map
    ]

    # Other required context
    projects = Project.objects.filter(team_members=employee, status='active')
    tasks = Task.objects.filter(assigned_to=employee).exclude(status='Completed')

    # Check if all days are already filled (so no form should show)
    already_filled_entire_week = len(week_data) == 0

    return render(request, 'timesheet_templates/timesheet.html', {
        'week_data': week_data,
        'projects': projects,
        'tasks': tasks,
        'existing_records': record_map,
        'already_filled_entire_week': already_filled_entire_week
    })

def daily_timesheet(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)
    projects = Project.objects.filter(team_members=employee, status='active')
    tasks = Task.objects.filter(assigned_to=employee).exclude(status='Completed')

    today = date.today()
    # Check if already filled for today (for any task)
    already_filled_today = TaskRecord.objects.filter(
        task__assigned_to=employee,
        date=today
    ).exists()

    if request.method == 'POST':
        project_id = request.POST.get('project')
        task_id = request.POST.get('task')
        date_val = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')
        upload_file = request.FILES.get('upload_file')

        errors = {}

        if not project_id:
            errors['project'] = "Project is required."
        if not task_id:
            errors['task_title'] = "Task is required."
        if not start_time:
            errors['start_time'] = "Start date is required."
        if not end_time:
            errors['end_time'] = "End date is required."
        if not description:
            errors['description'] = "Description is required."
            # Time check
            if start_time and end_time:
                try:
                    start_time = datetime.strptime(start_time, "%H:%M")
                    end_time = datetime.strptime(end_time, "%H:%M")
                    if start_time >= end_time:
                        errors["start"] = "Start time must be before end time."
                        errors["end"] = "End time must be after start time."
                except ValueError:
                    errors["start"] = "Invalid start time format."
                    errors["end"] = "Invalid end time format."

        # File size check
        if upload_file:
            # File size validation
            if upload_file.size > 2 * 1024 * 1024:
                errors['upload_file'] = "File size must not exceed 2MB."

            # File format validation
            ext = os.path.splitext(upload_file.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                errors['upload_file'] = "Invalid file format."



        if errors:
                return JsonResponse({'success': False, 'errors': errors},status=400)

        # Save the timesheet entry
        task = Task.objects.get(id=task_id)
        TaskRecord.objects.create(
            task =task,
            date=date_val or date.today(),
            start_time=start_time,
            end_time=end_time,
            record_name=description,
            attachment=upload_file
        )

        return JsonResponse({'success': True, 'message': 'Timesheet submitted successfully.'})

    return render(request, 'timesheet_templates/timesheet_daily.html', {
        'projects': projects,
        'tasks': tasks,
        'already_filled_today': already_filled_today,
    })


def image_timesheet(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            errors = {}


            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            upload_file = request.FILES.get('upload_file')

            # Validate upload file
            if upload_file:
                if upload_file.size > 2 * 1024 * 1024:  # 2MB limit
                    errors['upload_file'] = "File size must not exceed 2MB."
                else:
                    extension = os.path.splitext(upload_file.name)[1].lower()
                    if extension not in ALLOWED_EXTENSIONS:
                        errors['upload_file'] = "Invalid file format."
            else:
                errors['upload_file'] = "Please upload a file."

            if errors:
                return JsonResponse({'success': False, 'errors': errors}, status=400)

            # Save the record
            ImagetaskRecord.objects.create(
                start_date=start_date,
                end_date=end_date,
                file=upload_file,
                employee=employee,
            )

            return JsonResponse({
                'success': True,
                'message': 'Timesheet submitted successfully!',
                'data': {
                    'start_date': start_date,
                    'end_date': end_date,
                }
            })

        else:
            # If not an AJAX request
            return JsonResponse({'success': False, 'message': 'Invalid request. AJAX required.'}, status=400)

    # For GET request (load page)
    return render(request, 'timesheet_templates/timesheet_image.html')