# Generated by Django 4.1 on 2022-09-23 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='receives_alert_emails',
            field=models.BooleanField(default=False, help_text='Indicates whether user should receive email notifications of alarms'),
        ),
    ]
