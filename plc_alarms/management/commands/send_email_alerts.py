from django.core.management.base import BaseCommand

from plc_core.plc_alarms import send_alerts


class Command(BaseCommand):
    help = 'Process and send email alerts for PLC alarms'

    def add_arguments(self, parser):
        parser.add_argument('-d',
                            '--dry-run',
                            action='store_true',
                            help='Performs alarm processing but does not send email')

    def handle(self, *args, **options):
        try:
            dry_run = options['dry_run'] if options['dry_run'] else False
            send_alerts(dry_run)
        except Exception as e:
            self.stdout.write(e)
