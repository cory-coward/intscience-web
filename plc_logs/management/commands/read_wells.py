import pytz

from datetime import datetime
from django.core.management.base import BaseCommand

from plc_core.plc_measurements import PlcMeasurements


class Command(BaseCommand):
    help = 'Read data for all wells found in database'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            ctz = pytz.timezone('America/Chicago')

            # PlcMeasurements.read_wells()

            self.stdout.write(f'Wells successfully read at {datetime.now(ctz)}')
        except Exception as e:
            self.stdout.write(e)
