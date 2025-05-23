from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'Project'

urlpatterns = [
    #For Project
    path('project_add/page/', views.Project_add, name="project_add"),
    path('project_list/',views.Project_list,name='project_list'),
    path('project_add/',views.add_project,name='project_added'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('project/history/<int:pk>/', views.project_history_detail, name='projecthistory_detail'),
    path('Update/page/<int:id>/', views.Project_update_page, name='project_update_page'),
    path('Update/<int:id>/', views.update_project, name='Update_Project'),
    path('project/<int:project_id>/complete/', views.mark_project_completed, name='mark_completed'),
    path('get-project-employees/<int:project_id>/', views.get_project_employees, name='get_project_employees'),
    path('project/history/',views.Project_history,name='Project_History'),

    #For Task
    path('task_list/', views.Task_list, name='task_list'),
    path('task_add/page/', views.Task_add_page, name='task_add'),
    path('task_add/', views.add_Task, name='add_task'),
    path('task/<int:id>/', views.Task_detail, name='task_detail'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('task/update/page/<int:id>/', views.Task_update_page, name='task_update_page'),
    path('tasks/update/<int:id>/', views.update_task, name='update_task'),
    path('task/history/',views.Task_history,name='Task_History')


]