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
        self.model = "gpt-4"  # gpt-3.5-turbo or gpt-4
        self.history = [
                {"role": "system", "content": "You're Ruby, friendly helpful IT assistant, answer concisely and with natural language, in sentences"},
        ]

        if user_settings:
            self.history.append({"role": "system", "content": f"Here's the organization info:"})
            if user_settings.organization_name:
                self.history.append({"role": "system", "content": f"Org: {user_settings.organization_name}"})
            if user_settings.elevated_support_phone_number:
                self.history.append({"role": "system", "content": f"IT No.: {user_settings.elevated_support_phone_number}"})
            if user_settings.primary_os:
                self.history.append({"role": "system", "content": f"OS: {user_settings.primary_os}"})

            supported_applications = SupportedApplication.objects.filter(user_settings=user_settings)
            if supported_applications:
                app_names = ', '.join([app.name for app in supported_applications])
                self.history.append({"role": "system", "content": f"Supported Apps: {app_names}"})
    

    def process_input(self, user_input):
        logger.info(f"User input: {user_input}")

        supported_applications = SupportedApplication.objects.filter(user_settings=self.user_settings)

        # Check if any application is mentioned in the user input
        mentioned_applications = [app for app in supported_applications if app.name.lower() in user_input.lower()]

        if mentioned_applications:
            for app in mentioned_applications:
                self.history.append({"role": "user", "content": f"Here's some tickets from our documentation for {app}. I did not look at these and cannot look at these. Use them to help answer my question when I ask it"})
                examples = TroubleshootingExample.objects.filter(application=app)
                for example in examples:
                    self.history.append({"role": "user", "content": f"Issue: {example.issue_description} Fix: {example.resolution_process}"})

        # Add user input to the conversation history
        self.history.append({"role": "user", "content": user_input})

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
