# Generated by Django 4.1.7 on 2023-04-04 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportedApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_used', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('elevated_support_phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('primary_os', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('organization_name', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TroubleshootingExample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_description', models.TextField()),
                ('resolution_process', models.TextField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.supportedapplication')),
            ],
        ),
        migrations.AddField(
            model_name='supportedapplication',
            name='user_settings',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chatbot.usersettings'),
        ),
    ]
