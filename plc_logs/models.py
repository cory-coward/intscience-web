from django.db import models


class WellLogEntry(models.Model):
    well_name = models.CharField(max_length=25)
    gal_per_minute = models.FloatField(default=0)
    total_gal = models.FloatField(default=0)
    is_running = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Well Log Entry'
        verbose_name_plural = 'Well Log Entries'

    def __str__(self):
        return f'{self.well_name} {self.timestamp}'
