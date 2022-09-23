from django.db import models

from accounts.models import CustomUser


class MaintenanceLog(models.Model):
    log_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.author} {self.created_on}'


class GardnerDenverLog(models.Model):
    log_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.author} {self.created_on}'
