from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    receives_alert_emails = models.BooleanField(default=False,
                                                help_text='Indicates whether user should receive email notifications '
                                                          'of alarms')
    text_to_address = models.CharField(max_length=50,
                                       blank=True,
                                       help_text='Example: 5554441111@txt.att.net (Consult online for carrier-specific '
                                                 'information)')
    receives_text_alerts = models.BooleanField(default=False,
                                               help_text='Indicates whether user should receive text notifications '
                                                         'of alarms')

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
