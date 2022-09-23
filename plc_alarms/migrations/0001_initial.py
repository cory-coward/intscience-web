# Generated by Django 4.1 on 2022-08-12 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PLCAlarm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50)),
                ('is_cleared', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]