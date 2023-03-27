from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    elevated_support_phone_number = models.CharField(max_length=20, blank=True, null=True)
    primary_os = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    organization_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class SupportedApplication(models.Model):
    name = models.CharField(max_length=255)
    user_settings = models.ForeignKey(UserSettings, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TroubleshootingExample(models.Model):
    application = models.ForeignKey(SupportedApplication, on_delete=models.CASCADE)
    issue_description = models.TextField()
    resolution_process = models.TextField()

    def __str__(self):
        return f"Issue: {self.issue_description} In:{self.application.name} Resolved by: {self.issue_description}"
