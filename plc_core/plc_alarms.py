from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import List
import smtplib

from accounts.models import CustomUser
from plc_alarms.models import PLCAlarm

from .plc_item import PLCItem


class PlcAlarms:
    @staticmethod
    def process_alarms(plc_items: List[PLCItem]):
        # Load active alarms from db
        active_alarms = PLCAlarm.objects.filter(is_active=True).order_by('-timestamp')

        # Filter out items with an alarm from plc_items
        items_with_alarm = [x for x in plc_items if x.dial is True]

        # Loop through active_alarms
        for a in active_alarms:
            # alarm_matches contains newly recorded alarms that already exist in the db
            alarm_matches = [x for x in items_with_alarm if x.source_tag == a.tag_name and x.alarm_time == a.timestamp]

            if len(alarm_matches) > 0:
                # alarm_matches can only have one element since tag/timestamp are unique
                # Alarm is still active--update count and timestamps
                a.alarm_count = alarm_matches[0].alarm_count
                a.timestamp = alarm_matches[0].alarm_time
                a.timestamp_acknowledged = alarm_matches[0].ack_time
                a.timestamp_cleared = alarm_matches[0].clear_time

                # If there is a match, then remove from plc_items
                items_with_alarm.remove(alarm_matches[0])
            else:
                # alarm is not active - -set as inactive and update timestamps
                a.is_active = False

        # Remaining items in plc_items are not in db--save them
        new_alarms: List[PLCAlarm] = []
        for remaining_item in items_with_alarm:
            new_alarm = PLCAlarm()
            new_alarm.tag_name = remaining_item.source_tag
            new_alarm.is_active = True
            new_alarm.alarm_count = remaining_item.alarm_count
            new_alarm.timestamp = remaining_item.alarm_time

            new_alarms.append(new_alarm)

        # Commit changes to database
        PLCAlarm.objects.bulk_update(active_alarms,
                                     ['is_active', 'alarm_count', 'timestamp', 'timestamp_acknowledged',
                                      'timestamp_cleared', ])
        PLCAlarm.objects.bulk_create(new_alarms)

        # Send alert emails
        email_success: bool = PlcAlarms.send_alerts()

    @staticmethod
    def send_alerts() -> bool:
        # Load in all user emails who receive alarm emails
        alarm_recipients = CustomUser.objects.filter(receives_alert_emails=True)

        email_success: bool = True

        gmail_user = settings.GMAIL_USER
        gmail_password = settings.GMAIL_PASSWORD

        email_from: str = gmail_user
        email_to: List[str] = []

        for recipient in alarm_recipients:
            email_to.append(recipient.email)

        email_body: MIMEMultipart = MIMEMultipart('alternative')
        email_body['Subject'] = 'IST Grenada Alert'
        email_body['From'] = gmail_user

        email_text = f"""
            Hello,
            
            The following PLC tags have triggered an alarm:
        """

        email_body.attach(MIMEText(email_text, 'plain'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_password)
            # server.sendmail(email_from, email_to, email_body.as_string())
            server.close()
        except Exception as ex:
            print(ex)
            email_success = False

        # return response.status_code == 202
        return email_success
