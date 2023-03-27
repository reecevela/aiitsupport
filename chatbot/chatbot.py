import openai
from django.conf import settings
from .models import SupportedApplication, TroubleshootingExample

#included for development/testing only
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('chatbot_logs.txt')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
#end logging declaration

openai.api_key = settings.OPENAI_API_KEY

class ChatBot:
    def __init__(self, user_settings=None):
        self.user_settings = user_settings
        self.model = "gpt-3.5-turbo"  # gpt-3.5-turbo
        self.history = [
            {"role": "system", "content": "You are a helpful IT Support assistant named Ruby, answer as concisely as possible."},
        ]

        if user_settings:
            if user_settings.organization_name:
                self.history.append({"role": "system", "content": f"Organization: {user_settings.organization_name}"})
            if user_settings.elevated_support_phone_number:
                self.history.append({"role": "system", "content": f"Elevated support number: {user_settings.elevated_support_phone_number}"})
            if user_settings.primary_os:
                self.history.append({"role": "system", "content": f"Primary OS: {user_settings.primary_os}"})

            supported_applications = SupportedApplication.objects.filter(user_settings=user_settings)
            if supported_applications:
                app_names = ', '.join([app.name for app in supported_applications])
                self.history.append({"role": "system", "content": f"Supported applications: {app_names}"})

    def process_input(self, user_input):
        # Add user input to the conversation history
        self.history.append({"role": "user", "content": user_input})
        logger.info(f"User input: {user_input}")

        supported_applications = SupportedApplication.objects.filter(user_settings=self.user_settings)

        # Check if any application is mentioned in the user input
        mentioned_applications = [app for app in supported_applications if app.name.lower() in user_input.lower()]

        if mentioned_applications:
            for app in mentioned_applications:
                examples = TroubleshootingExample.objects.filter(application=app)
                for example in examples:
                    self.history.append({"role": "assistant", "content": f"Issue: {example.issue_description} - Resolution: {example.resolution_process}"})

        api_response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.history
        )

        chat_response = api_response["choices"][0]["message"]["content"]

        # Add AI response to the conversation history
        self.history.append({"role": "assistant", "content": chat_response})
        logger.info(f"AI response: {chat_response}")
        logger.info(f"History: {self.history}")

        return chat_response
