# Generated by Django 4.1 on 2022-09-27 17:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('well_record_minutes', models.PositiveIntegerField(default=10, help_text='How many minutes between saving well readings to database, between 10 and 360', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(360)])),
            ],
            options={
                'verbose_name': 'General Configuration',
                'verbose_name_plural': 'General Configuration Entries',
            },
        ),
        migrations.CreateModel(
            name='WellConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('well_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('tag_prefix', models.CharField(max_length=50)),
                ('cycle_gallons', models.PositiveIntegerField(help_text='Gallons per cycle')),
                ('sleep_minutes', models.PositiveIntegerField(help_text='Minutes to sleep before restarting cycle')),
            ],
            options={
                'verbose_name': 'Well Configuration',
                'verbose_name_plural': 'Well Configuration Entries',
            },
        ),
        migrations.AddConstraint(
            model_name='generalconfig',
            constraint=models.CheckConstraint(check=models.Q(('well_record_minutes__range', (10, 360))), name='plc_config_WellConfig_well_record_minutes_range'),
        ),
    ]
