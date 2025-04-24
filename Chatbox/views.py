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


def chat_page(request, project_id):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return HttpResponseNotFound("Project not found")

    return render(request, 'Chatbox/chat_page.html', {
        'project': project
    })


def send_message(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    emp_id = request.session.get('employee_id')
    if not emp_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    employee = EmployeeBISP.objects.get(id=emp_id)

    if request.method == 'POST':
        text = request.POST.get("message")
        project_id = request.POST.get("project_id")

        if not text or not project_id:
            return JsonResponse({'error': 'Missing message or project'}, status=400)

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Project not found'}, status=404)

        if employee not in project.team_members.all() and employee != project.leader and employee != project.admin:
            return JsonResponse({'error': 'Access denied'}, status=403)

        Message.objects.create(user=employee, text=text, project=project)
        return JsonResponse({'status': 'success'})

    return JsonResponse({'error': 'Invalid method'}, status=405)


def get_messages(request):
    if not request.session.get('employee_id'):
        return redirect('Login_user_page')
    emp_id = request.session.get('employee_id')
    if not emp_id:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    employee = EmployeeBISP.objects.get(id=emp_id)
    last_id = int(request.GET.get("last_id", 0))
    project_id = request.GET.get("project_id")

    if not project_id:
        return JsonResponse({'error': 'Missing project_id'}, status=400)

    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    if employee not in project.team_members.all() and employee != project.leader and employee != project.admin:
        return JsonResponse({'error': 'Access denied'}, status=403)

    messages = Message.objects.filter(project=project, id__gt=last_id).order_by("id")

    data = {
        "messages": [
            {
                "id": msg.id,
                "user": msg.user.username,
                "content": msg.text,
                "timestamp": msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }
            for msg in messages
        ]
    }
    return JsonResponse(data)
