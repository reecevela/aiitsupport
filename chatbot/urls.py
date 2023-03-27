from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chatbot, name='chatbot'),
    path('api/', views.api_chatbot, name='api_chatbot'),
    path('settings/', views.settings, name='settings'),
    path('examples/', views.add_troubleshooting_example, name='add_troubleshooting_example'),
    path('apps/', views.add_supported_application, name='add_supported_application'),
]
