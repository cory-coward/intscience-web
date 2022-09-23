from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class WellConfig(models.Model):
    well_name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    tag_prefix = models.CharField(max_length=50, help_text='')
    cycle_gallons = models.PositiveIntegerField(help_text='Gallons per cycle')
    sleep_minutes = models.PositiveIntegerField(help_text='Minutes to sleep before restarting cycle')
    record_minutes = models.PositiveIntegerField(default=10,
                                                 help_text='How many minutes between saving readings to database, '
                                                           'between 10 and 360',
                                                 validators=[MinValueValidator(10), MaxValueValidator(360)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='plc_config_WellConfig_record_minutes_range',
                check=models.Q(record_minutes__range=(10, 360))
            )
        ]

    def __str__(self):
        return self.well_name
