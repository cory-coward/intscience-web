from django.db import models


class PLCAlarm(models.Model):
    tag_name = models.CharField(max_length=50)
    is_suppressed = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    timestamp_cleared = models.DateTimeField()

    def __str__(self):
        return self.tag_name
