from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import TaskRecord
from HR_App.models import EmployeeBISP
from Project.models import Task,Project
from datetime import date
from django.views.decorators.csrf import csrf_exempt


def timesheet_record(request):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    dates = [monday + timedelta(days=i) for i in range(7)]

    records = TaskRecord.objects.filter(date__range=(monday, monday + timedelta(days=6)))


    return render(request,'timesheet_templates/timesheet_record.html', {
        'dates': dates,
        'records': records,
    })


def get_week_dates(last_week=False):
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    if last_week:
        monday -= timedelta(days=7)
    return [monday + timedelta(days=i) for i in range(6)]  # Mon to Sun


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
            if project_id:
                at_least_one_filled = True  # Mark that a valid row is attempted

                if not task_id:
                    day_errors["task"] = "Task is required."
                if not date:
                    day_errors["date"] = "Date is required."
                if not start:
                    day_errors["start"] = "Start time is required."
                if not end:
                    day_errors["end"] = "End time is required."
                if not desc:
                    day_errors["description"] = "Description is required."

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
    week_data = [{'day': d.strftime('%A'), 'date': d.strftime('%Y-%m-%d')} for d in get_week_dates(last_week)]
    projects = Project.objects.filter(team_members=employee)
    tasks = Task.objects.filter(assigned_to=employee)

    return render(request, 'timesheet_templates/timesheet.html', {
        'week_data': week_data,
        'projects': projects,
        'tasks': tasks
    })

def daily_timesheet(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session['employee_id']
    employee = EmployeeBISP.objects.get(id=emp_id)

    projects = Project.objects.filter(team_members=employee)
    tasks = Task.objects.filter(assigned_to=employee)
    return render(request,'timesheet_templates/timesheet_daily.html',{'projects':projects,'tasks': tasks})