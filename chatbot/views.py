from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .chatbot import ChatBot
from .freechatbot import ChatBotFree
from .forms import UserSettingsForm, TroubleshootingExampleForm, SupportedApplicationForm
from .models import UserSettings, SupportedApplication, TroubleshootingExample
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        subject = f'Message from {name}'
        message = f'From: {name} <{email}>\n\n{message}'

        send_mail(subject, message, 'reecevela@outlook.com', ['reecevela@outlook.com'])

        return render(request, 'homepage/index.html')
    return render(request, 'homepage/index.html')


free_chatbot_instance = ChatBotFree()

def api_free_chatbot(request):
    if request.method == "POST":
        user_input = request.POST.get('user_input')
        chat_response = free_chatbot_instance.process_input(user_input)
       
        if chat_response:
            return JsonResponse({
                'response': chat_response,
            })
        else:
            return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)
    else:
        return HttpResponseForbidden("Invalid request method.")

def home(request):
    return render(request, 'homepage/index.html')

def privacy(request):
<<<<<<< HEAD
    return render(request, 'homepage/privacy_policy.html')
=======
    return render(request, 'homepage/index.html')
>>>>>>> 1bcf9083542d3c75a1146163bf48ec14909c18f3

@login_required
def chatbot(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
    supported_applications = SupportedApplication.objects.filter(user_settings=user_settings)
    form = TroubleshootingExampleForm()
    return render(request, 'chatbot/chatbot.html', {
        'user_settings': user_settings,
        'supported_applications': supported_applications,
        'troubleshooting_example_form': form,
    })

@login_required
def api_chatbot(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to use the chatbot.")

    user_input = request.POST.get('user_input')
    conversation_history_raw = request.POST.get('conversation_history')
    
    # Check if conversation_history_raw is None and set it to an empty list if necessary
    conversation_history = json.loads(conversation_history_raw) if conversation_history_raw else []

    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
    chatbot_instance = ChatBot(user_settings)

    # Set the conversation history
    chatbot_instance.history = conversation_history_to_chatbot_format(conversation_history)

    chat_response = chatbot_instance.process_input(user_input)

    return JsonResponse({
        'response': chat_response,
    })

def conversation_history_to_chatbot_format(conversation_history):
    chatbot_history = []

    for message in conversation_history:
        role, content = message.split(': ', 1)

        if role == 'You':
            chatbot_history.append({"role": "user", "content": content})
        elif role == 'Ruby':
            chatbot_history.append({"role": "assistant", "content": content})

    return chatbot_history


@login_required
def settings(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            user_settings = form.save()
            return redirect('chatbot:chatbot')
    else:
        form = UserSettingsForm(instance=user_settings)

    return render(request, 'chatbot/settings.html', {'form': form})

@login_required
def add_troubleshooting_example(request):
    if request.method == 'POST':
        form = TroubleshootingExampleForm(request.POST)
        if form.is_valid():
            new_example = form.save()
            return redirect('chatbot:chatbot')
    else:
        form = TroubleshootingExampleForm()

    return render(request, 'chatbot/troubleshooting.html', {'form': form})

@login_required
def add_supported_application(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = SupportedApplicationForm(request.POST)
        if form.is_valid():
            new_application = form.save(commit=False)
            new_application.user_settings = user_settings
            new_application.save()
            return redirect('chatbot:chatbot')
    else:
        form = SupportedApplicationForm()

    return render(request, 'chatbot/settings.html', {'form': form})
