from django.db import models


class WellLogEntry(models.Model):
    AUTO = 'auto'
    MANUAL = 'manual'

    PUMP_MODE_CHOICES = (
        (AUTO, 'Auto'),
        (MANUAL, 'Manual'),
    )

    well_name = models.CharField(max_length=25)
    gal_per_minute = models.DecimalField(max_digits=10, decimal_places=1, default=0, null=True, blank=True)
    total_gal = models.DecimalField(max_digits=10, decimal_places=1, default=0, null=True, blank=True)
    pump_mode = models.CharField(max_length=20, choices=PUMP_MODE_CHOICES, default=AUTO)
    is_running = models.BooleanField(default=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Well Log Entry'
        verbose_name_plural = 'Well Log Entries'

    def __str__(self):
        return f'{self.well_name} {self.timestamp}'


class AirStripperLogEntry(models.Model):
    air_stripper_name = models.CharField(max_length=25)
    pump_runtime = models.DecimalField(max_digits=10, decimal_places=1, default=0, null=True, blank=True,
                                       verbose_name='Pump Runtime')
    blower_runtime = models.DecimalField(max_digits=10, decimal_places=1, default=0, null=True, blank=True,
                                         verbose_name='Blower Runtime')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Air Stripper Log Entry'
        verbose_name_plural = 'Air Stripper Log Entries'

    def __str__(self):
        return f'{self.air_stripper_name} {self.timestamp}'
