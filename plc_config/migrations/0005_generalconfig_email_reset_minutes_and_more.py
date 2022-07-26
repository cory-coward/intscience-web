# Generated by Django 4.1.2 on 2022-11-01 15:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plc_config', '0004_airstripperconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalconfig',
            name='email_reset_minutes',
            field=models.PositiveIntegerField(default=10, help_text='How many minutes to wait before resending alertemails, between 10 and 360', validators=[django.core.validators.MinValueValidator(10), django.core.validators.MaxValueValidator(360)]),
        ),
        migrations.AddConstraint(
            model_name='generalconfig',
            constraint=models.CheckConstraint(check=models.Q(('email_reset_minutes__range', (10, 360))), name='plc_config_email_reset_minutes_range'),
        ),
    ]
