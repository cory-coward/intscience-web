import pytz

from datetime import datetime
from django.core.management.base import BaseCommand

from plc_core.plc_ops import read_plc_tags


class Command(BaseCommand):
    help = 'Read data for PLC'

    def add_arguments(self, parser):
        parser.add_argument('-i',
                            '--ignore-period',
                            action='store_true',
                            help='Forces plc readings to be recorded in database',)

    def handle(self, *args, **options):
        try:
            ctz = pytz.timezone('America/Chicago')

            ignore_period = options['ignore_period'] if options['ignore_period'] else False
            read_plc_tags(ignore_period)

            self.stdout.write(f'PLC tags successfully read at {datetime.now(ctz)}')
        except Exception as e:
            self.stdout.write(e)
