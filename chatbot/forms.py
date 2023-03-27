from django import forms
from .models import UserSettings, SupportedApplication, TroubleshootingExample

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = [
            'elevated_support_phone_number',
            'primary_os',
            'city',
            'state',
            'organization_name',
        ]

class SupportedApplicationForm(forms.ModelForm):
    class Meta:
        model = SupportedApplication
        fields = ['name', 'is_used']

class TroubleshootingExampleForm(forms.ModelForm):
    class Meta:
        model = TroubleshootingExample
        fields = ['application', 'issue_description', 'resolution_process']
