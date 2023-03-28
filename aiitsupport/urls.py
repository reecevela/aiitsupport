from django.contrib import admin
from django.urls import path, include
from chatbot.views import home, api_free_chatbot, send_email
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home),
    path('contact', home),
    path('admin/', admin.site.urls),
    path('send_email/', send_email, name='send_email'),
    path('chatbot/', include('chatbot.urls', namespace='chatbot')),
    path('api/free_chatbot/', api_free_chatbot, name='api_free_chatbot'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
