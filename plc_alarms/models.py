from django.db import models


class PLCAlarm(models.Model):
    tag_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    alarm_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(null=True, blank=True)
    timestamp_acknowledged = models.DateTimeField(null=True, blank=True)
    timestamp_cleared = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'PLC Alarm'
        verbose_name_plural = 'PLC Alarms'
        constraints = [
            models.UniqueConstraint(fields=['tag_name', 'timestamp', ], name='unique_tag_name_timestamp'),
        ]

    def __str__(self):
        return f'{self.tag_name} {self.timestamp}'
