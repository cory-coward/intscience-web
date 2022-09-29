from django.conf import settings
from typing import List
import sendgrid
from sendgrid.helpers.mail import Content, Email, Mail, Personalization
from accounts.models import CustomUser
from plc_alarms.models import PLCAlarm

from .plc_measurements import PLCItem


class PlcAlarms:
    @staticmethod
    def process_alarms(plc_items: List[PLCItem]):
        # Load active alarms from db
        active_alarms = PLCAlarm.objects.filter(is_active=True).order_by('-timestamp')

        # Loop through active_alarms
        for a in active_alarms:
            # alarm_matches contains newly recorded alarms that already exist in the db
            alarm_matches = [x for x in plc_items if x.source_tag == a.tag_name and x.alarm_time == a.timestamp]

            if len(alarm_matches) > 0:
                # alarm_matches can only have one element since tag/timestamp are unique
                # Alarm is still active--update count and timestamps
                a.alarm_count = alarm_matches[0].alarm_count
                a.timestamp = alarm_matches[0].alarm_time
                a.timestamp_acknowledged = alarm_matches[0].ack_time
                a.timestamp_cleared = alarm_matches[0].clear_time

                # If there is a match, then remove from plc_items
                plc_items.remove(alarm_matches[0])
            else:
                # alarm is not active - -set as inactive and update timestamps
                a.is_active = False

        # Remaining items in plc_items are not in db--save them
        new_alarms: List[PLCAlarm] = []
        for remaining_item in plc_items:
            new_alarm = PLCAlarm()
            new_alarm.tag_name = remaining_item.source_tag
            new_alarm.is_active = True
            new_alarm.alarm_count = remaining_item.alarm_count
            new_alarm.timestamp = remaining_item.alarm_time

            new_alarms.append(new_alarm)

        # Commit changes to database
        PLCAlarm.objects.bulk_update(active_alarms)
        PLCAlarm.objects.bulk_create(new_alarms)

        # Send alert emails
        email_success: bool = PlcAlarms.send_alerts()

    @staticmethod
    def send_alerts() -> bool:
        # Load in all user emails who receive alarm emails
        alarm_recipients = CustomUser.objects.filter(receives_alert_emails=True)

        # Configure alarm email information
        sg = sendgrid.SendGridAPIClient(
            api_key=settings.SENDGRID_API_KEY
        )
        subject = f'IST - Grenada Alert'
        from_email = Email('from@email.com')
        content = Content('text/plain', 'Email content goes here')
        mail = Mail(from_email, subject, None, content)

        for recipient in alarm_recipients:
            r = Personalization()
            r.add_to(Email(recipient.email))
            mail.add_personalization(r)

        # Send emails
        response = sg.client.mail.send.post(request_body=mail.get())

        return response.status_code == 202
