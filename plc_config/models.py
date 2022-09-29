from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GeneralConfig(models.Model):
    well_record_minutes = models.PositiveIntegerField(default=10,
                                                      help_text='How many minutes between saving well readings to '
                                                                'database, between 10 and 360',
                                                      validators=[MinValueValidator(10), MaxValueValidator(360)])

    class Meta:
        verbose_name = 'General Configuration'
        verbose_name_plural = 'General Configuration Entries'
        constraints = [
            models.CheckConstraint(
                name='plc_config_WellConfig_well_record_minutes_range',
                check=models.Q(well_record_minutes__range=(10, 360))
            )
        ]

    def __str__(self):
        return f'General configuration {self.pk}'


class WellConfig(models.Model):
    well_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    tag_prefix = models.CharField(max_length=50, help_text='')
    cycle_gallons = models.PositiveIntegerField(help_text='Gallons per cycle')
    sleep_minutes = models.PositiveIntegerField(help_text='Minutes to sleep before restarting cycle')

    class Meta:
        verbose_name = 'Well Configuration'
        verbose_name_plural = 'Well Configuration Entries'

    def __str__(self):
        return self.well_name
