from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class GeneralConfig(models.Model):
    well_record_minutes = models.PositiveIntegerField(default=10,
                                                      help_text='How many minutes between saving well readings to '
                                                                'database, between 10 and 360',
                                                      validators=[MinValueValidator(10), MaxValueValidator(360)])
    email_reset_minutes = models.PositiveIntegerField(default=10,
                                                      help_text='How many minutes to wait before resending alert'
                                                                'emails, between 10 and 360',
                                                      validators=[MinValueValidator(10), MaxValueValidator(360)])

    class Meta:
        verbose_name = 'General Configuration'
        verbose_name_plural = 'General Configuration Entries'
        constraints = [
            models.CheckConstraint(
                name='plc_config_WellConfig_well_record_minutes_range',
                check=models.Q(well_record_minutes__range=(10, 360))
            ),
            models.CheckConstraint(
                name='plc_config_email_reset_minutes_range',
                check=models.Q(email_reset_minutes__range=(10, 360))
            )
        ]

    def __str__(self):
        return f'General configuration {self.pk}'


class WellConfig(models.Model):
    well_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    tag_prefix = models.CharField(max_length=50, help_text='The tag name as it appears in the PLC')
    cycle_gallons = models.FloatField(default=0, help_text='Gallons per cycle')
    sleep_minutes = models.FloatField(default=0, help_text='Minutes to sleep before restarting cycle')

    class Meta:
        verbose_name = 'Well Configuration'
        verbose_name_plural = 'Well Configuration Entries'

    def __str__(self):
        return self.well_name


class AirStripperConfig(models.Model):
    air_stripper_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    tag_prefix = models.CharField(max_length=50, help_text='The tag name as it appears in the PLC')

    class Meta:
        verbose_name = 'Air Stripper Configuration'
        verbose_name_plural = 'Air Stripper Configuration Entries'

    def __str__(self):
        return self.air_stripper_name
