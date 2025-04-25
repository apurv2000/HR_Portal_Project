from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'Timesheet'

urlpatterns = [

    path('timesheet_add/', views.timesheet_add, name="timesheet_add"),
    path('timesheet_record/', views.timesheet_record, name="timesheet_record"),
    path('timesheet_daily/', views.daily_timesheet, name="timesheet_daily"),

]