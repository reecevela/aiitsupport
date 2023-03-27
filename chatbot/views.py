from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .chatbot import ChatBot
from .freechatbot import ChatBotFree
from .forms import UserSettingsForm, TroubleshootingExampleForm, SupportedApplicationForm
from .models import UserSettings, SupportedApplication, TroubleshootingExample
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt

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

        return JsonResponse({
            'response': chat_response,
        })
    else:
        return HttpResponseForbidden("Invalid request method.")


def home(request):
    return render(request, 'homepage/index.html')

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
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
    chatbot_instance = ChatBot(user_settings)
    chat_response = chatbot_instance.process_input(user_input)

    return JsonResponse({
        'response': chat_response,
    })


@login_required
def settings(request):
    user_settings, _ = UserSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=user_settings)
        if form.is_valid():
            # Save the user's other settings
            user_settings = form.save(commit=False)
            user_settings.save()
            
            # Update the supported applications list
            new_app = request.POST.get('new_app', '').strip()
            if new_app:
                user_settings.supported_applications.append(new_app)
                user_settings.save()
            
            return redirect('chatbot:chatbot')
    else:
        form = UserSettingsForm(instance=user_settings)

    return render(request, 'chatbot/settings.html', {'form': form})


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