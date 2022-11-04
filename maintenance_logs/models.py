from django.db import models
from django.urls import reverse

from accounts.models import CustomUser


class MaintenanceLog(models.Model):
    log_text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Maintenance Log'
        verbose_name_plural = 'Maintenance Logs'

    def __str__(self):
        return f'{self.author} {self.created_on}'

    def get_absolute_url(self):
        return reverse('maintenance_logs:maintenance-log-detail', args=[str(self.pk)])


class GardnerDenverLog(models.Model):
    advisory_number = models.CharField(max_length=100, blank=True, verbose_name='Service, Codes, or Advisory Number')
    blower_hours = models.FloatField(null=True, blank=True, verbose_name='Blower, Hours')
    bar_pressure = models.FloatField(null=True, blank=True, verbose_name='Barometric Pressure (in Hg)')
    blower_post_vacuum = models.FloatField(null=True,
                                           blank=True,
                                           verbose_name='Blower Intake Post-Air Filter Vacuum (in Hg)')
    blower_exhaust_temp = models.FloatField(null=True, blank=True, verbose_name='Blower Exhaust Temperature (deg F)')
    zone_1_2_flow = models.FloatField(null=True, blank=True, verbose_name='Zone 1 & 2 Flow (calculated 4", cfm)')
    combined_flow = models.FloatField(null=True, blank=True, verbose_name='Combined Flow (calculated 8", cfm)')
    pid_cv_influent = models.FloatField(null=True, blank=True, verbose_name='PID CV Influent (ppm)')
    pid_mid_carbon = models.FloatField(null=True, blank=True, verbose_name='PID Mid Carbon (ppm)')
    pid_cv_effluent = models.FloatField(null=True, blank=True, verbose_name='PID CV Effluent (emission, ppm)')
    pressure_cv_influent = models.FloatField(null=True, blank=True, verbose_name='Pressure CV Influent (in H2O)')
    pressure_bet_cvs = models.FloatField(null=True, blank=True, verbose_name='Pressure Between CVs (in H2O)')
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Gardner Denver Log'
        verbose_name_plural = 'Gardner Denver Logs'

    def __str__(self):
        return f'{self.author} {self.created_on}'

    def get_absolute_url(self):
        return reverse('maintenance_logs:gardner-denver-log-detail', args=[str(self.pk)])
