import pytz

from datetime import datetime
from django.core.management.base import BaseCommand

from plc_core.plc_well_ops import PlcMeasurements


class Command(BaseCommand):
    help = 'Read data for all wells found in database'

    def add_arguments(self, parser):
        parser.add_argument('-i',
                            '--ignore-period',
                            action='store_true',
                            help='Forces well readings to be recorded in database',)

    def handle(self, *args, **options):
        try:
            ctz = pytz.timezone('America/Chicago')

            ignore_period = options['ignore_period'] if options['ignore_period'] else False
            PlcMeasurements.read_wells(ignore_period)

            self.stdout.write(f'Wells successfully read at {datetime.now(ctz)}')
        except Exception as e:
            self.stdout.write(e)
