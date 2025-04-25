from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from .models import Message
from django.utils.timezone import now
# chat/views.py
from HR_App.models import EmployeeBISP
from Project.models import Project
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def chat_page(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session.get('employee_id')
    employee = EmployeeBISP.objects.get(id=emp_id)

    # Get the first project the employee is part of
    project = Project.objects.filter(team_members=employee).union(
        Project.objects.filter(leader=employee)
    ).union(
        Project.objects.filter(admin=employee)
    ).first()

    if not project:
        return HttpResponseNotFound("No associated project found for this employee.")

    return render(request, 'chatbox_templates/Chatbox.html', {
        'project': project
    })



def send_message(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session.get('employee_id')
    employee = EmployeeBISP.objects.get(id=emp_id)

    if request.method == 'POST':
        text = request.POST.get("message")

        if not text:
            return JsonResponse({'error': 'Missing message text'}, status=400)

        # Find the employee's first associated project
        project = Project.objects.filter(team_members=employee).union(
            Project.objects.filter(leader=employee)
        ).union(
            Project.objects.filter(admin=employee)
        ).first()

        if not project:
            return JsonResponse({'error': 'No associated project found'}, status=404)

        Message.objects.create(user=employee, text=text, project=project)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid method'}, status=405)


def get_messages(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    emp_id = request.session.get('employee_id')
    employee = EmployeeBISP.objects.get(id=emp_id)
    last_id = int(request.GET.get("last_id", 0))

    # Get the employee's associated project
    project = Project.objects.filter(team_members=employee).union(
        Project.objects.filter(leader=employee)
    ).union(
        Project.objects.filter(admin=employee)
    ).first()

    if not project:
        return JsonResponse({'error': 'No associated project found'}, status=404)

    messages = Message.objects.filter(project=project, id__gt=last_id).order_by("id")

    data = {
        "messages": [
            {
                "id": msg.id,
                "user": msg.user.name,
                "content": msg.text,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for msg in messages
        ]
    }
    return JsonResponse(data)
