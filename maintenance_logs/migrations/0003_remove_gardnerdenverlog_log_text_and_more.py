# Generated by Django 4.1.2 on 2022-11-04 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance_logs', '0002_alter_gardnerdenverlog_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gardnerdenverlog',
            name='log_text',
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='advisory_number',
            field=models.CharField(blank=True, max_length=100, verbose_name='Service, Codes, or Advisory Number'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='bar_pressure',
            field=models.FloatField(blank=True, null=True, verbose_name='Barometric Pressure (in Hg)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='blower_exhaust_temp',
            field=models.FloatField(blank=True, null=True, verbose_name='Blower Exhaust Temperature (deg F)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='blower_hours',
            field=models.FloatField(blank=True, null=True, verbose_name='Blower, Hours'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='blower_post_vacuum',
            field=models.FloatField(blank=True, null=True, verbose_name='Blower Intake Post-Air Filter Vacuum (in Hg)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='combined_flow',
            field=models.FloatField(blank=True, null=True, verbose_name='Combined Flow (calculated 8", cfm)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='pid_cv_effluent',
            field=models.FloatField(blank=True, null=True, verbose_name='PID CV Effluent (emission, ppm)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='pid_cv_influent',
            field=models.FloatField(blank=True, null=True, verbose_name='PID CV Influent (ppm)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='pid_mid_carbon',
            field=models.FloatField(blank=True, null=True, verbose_name='PID Mid Carbon (ppm)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='pressure_bet_cvs',
            field=models.FloatField(blank=True, null=True, verbose_name='Pressure Between CVs (in H2O)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='pressure_cv_influent',
            field=models.FloatField(blank=True, null=True, verbose_name='Pressure CV Influent (in H2O)'),
        ),
        migrations.AddField(
            model_name='gardnerdenverlog',
            name='zone_1_2_flow',
            field=models.FloatField(blank=True, null=True, verbose_name='Zone 1 & 2 Flow (calculated 4", cfm)'),
        ),
    ]
