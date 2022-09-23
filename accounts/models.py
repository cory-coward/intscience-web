from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    receives_alert_emails = models.BooleanField(default=False,
                                                help_text='Indicates whether user should receive email notifications '
                                                          'of alarms')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
