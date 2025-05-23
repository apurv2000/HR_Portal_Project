from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'Chatbox'

urlpatterns = [
    #For Chatbox

    path('view/', views.chat_page, name='chat'),
    path('send/', views.send_message, name='send_message'),
    path('get/', views.get_messages, name='get_messages'),
]
