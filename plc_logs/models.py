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


class ZoneFlowLogEntry(models.Model):
    zone_flow_right = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True,
                                          verbose_name='Zone 1 and 2 Flow Right Side')
    zone_flow_left = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True,
                                         verbose_name='Combined Flow (Left Side)')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Zone Flow Log Entry'
        verbose_name_plural = 'Zone Flow Log Entries'

    def __str__(self):
        return f'Zone Flow Log {self.timestamp}'


class GardnerDenverBlowerLogEntry(models.Model):
    intake_pre_air_filter_vacuum = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True,
                                                       blank=True, verbose_name='HE Discharge Pressure')
    intake_temp = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True,
                                      verbose_name='Intake Temperature')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Gardner Denver Blower Log Entry'
        verbose_name_plural = 'Gardner Denver Blower Log Entries'

    def __str__(self):
        return f'Gardner Denver Log {self.timestamp}'


class HeatExchangerLogEntry(models.Model):
    flow_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    flow_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    pressure = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True,
                                   verbose_name='SSDS Blower Vacuum')
    outlet_air_temp = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True,
                                          verbose_name='HE Discharge Temperature')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Heat Exchanger Log Entry'
        verbose_name_plural = 'Heat Exchanger Log Entries'

    def __str__(self):
        return f'Heat Exchanger Log {self.timestamp}'


class SurgeTankLogEntry(models.Model):
    flow_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    flow_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Surge Tank Log Entry'
        verbose_name_plural = 'Surge Tank Log Entries'

    def __str__(self):
        return f'Surge Tank Log {self.timestamp}'


class DischargeWaterLogEntry(models.Model):
    flow_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    flow_total = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Discharge Water Log Entry'
        verbose_name_plural = 'Discharge Water Log Entries'

    def __str__(self):
        return f'Discharge Water Log {self.timestamp}'
