from datetime import datetime
from typing import List
import os
import pytz
import smtplib

from django.conf import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from accounts.models import CustomUser
from plc_alarms.models import PLCAlarm
from plc_config.models import GeneralConfig
from plc_core.alarm_descriptions import alarm_descriptions
from plc_core.plc_core import PlcCore
from plc_core.plc_items import PlcAlarmItem


def process_alarms():
    alarm_tag_array_length: int = len(alarm_descriptions)
    plc_datetime_format = '%m/%d/%Y %H:%M:%S'
    ctz = pytz.timezone('America/Chicago')

    # Read alarms from PLC
    plc = PlcCore(ip_address=settings.PLC_IP)
    active_tag_array = plc.read_tag(tag_name='HMI.AlarmActive[0]', num_elements=alarm_tag_array_length)
    dial_tag_array = plc.read_tag(tag_name='HMI.AlarmDial[0]', num_elements=alarm_tag_array_length)
    alarm_time_tag_array = plc.read_tag(tag_name='HMI.AlarmTime[0]', num_elements=alarm_tag_array_length)
    ack_time_tag_array = plc.read_tag(tag_name='HMI.AckTime[0]', num_elements=alarm_tag_array_length)
    clear_time_tag_array = plc.read_tag(tag_name='HMI.ClearTime[0]', num_elements=alarm_tag_array_length)

    # Create list of PlcAlarmItem from tag array results
    current_active_alarms: List[PlcAlarmItem] = []
    for i in range(len(alarm_descriptions)):
        if active_tag_array.Value[i] is False:
            continue

        tag_name = alarm_descriptions[i].split(':')[0]
        tag_description = alarm_descriptions[i].split(':')[1]

        raw_alarm_time = alarm_time_tag_array.Value[i] or None
        raw_ack_time = ack_time_tag_array.Value[i] or None
        raw_clear_time = clear_time_tag_array.Value[i] or None

        item: PlcAlarmItem = PlcAlarmItem(
            alarm_tag=tag_name,
            alarm_description=tag_description,
            dial=dial_tag_array.Value[i],
            alarm_time=datetime.strptime(raw_alarm_time, plc_datetime_format).replace(tzinfo=ctz)
            if raw_alarm_time is not None else None,
            ack_time=datetime.strptime(raw_ack_time, plc_datetime_format).replace(tzinfo=ctz)
            if raw_ack_time is not None else None,
            clear_time=datetime.strptime(raw_clear_time, plc_datetime_format).replace(tzinfo=ctz)
            if raw_clear_time is not None else None,
        )

        current_active_alarms.append(item)

    # Load active alarms from db
    active_alarms_in_db = PLCAlarm.objects.filter(is_active=True).order_by('-timestamp')

    # Loop through active_alarms
    for a in active_alarms_in_db:
        # alarm_matches contains newly recorded alarms that already exist in the db
        alarm_matches = [x for x in current_active_alarms
                         if x.alarm_tag == a.tag_name and x.alarm_time == a.timestamp]

        if len(alarm_matches) > 0:
            # alarm_matches can only have one element since tag/timestamp are unique
            # Alarm is still active--update count and timestamps
            a.timestamp = alarm_matches[0].alarm_time
            a.timestamp_acknowledged = alarm_matches[0].ack_time
            a.timestamp_cleared = alarm_matches[0].clear_time

            # If there is a match, then remove from plc_items
            current_active_alarms.remove(alarm_matches[0])
        else:
            # alarm is not active - set as inactive and update timestamps
            a.is_active = False

    # Remaining items in plc_items are not in db--save them
    new_alarms: List[PLCAlarm] = []
    for remaining_item in current_active_alarms:
        new_alarm = PLCAlarm()
        new_alarm.tag_name = remaining_item.alarm_tag
        new_alarm.description = remaining_item.alarm_description
        new_alarm.receives_alerts = remaining_item.dial
        new_alarm.is_active = True
        new_alarm.timestamp = remaining_item.alarm_time

        new_alarms.append(new_alarm)

    # Commit changes to database
    PLCAlarm.objects.bulk_update(active_alarms_in_db,
                                 ['is_active', 'alarm_count', 'timestamp', 'timestamp_acknowledged',
                                  'timestamp_cleared', ])
    PLCAlarm.objects.bulk_create(new_alarms)


def send_alerts(dry_run: bool = False):
    # Check if any alarms need to be processed and bail if zero
    unprocessed_alarms_count = PLCAlarm.objects.filter(is_active=True).count()

    if unprocessed_alarms_count == 0:
        print('No alarms to process.')
        return

    # Load in all user emails who receive alarm emails
    email_recipients = CustomUser.objects.filter(receives_alert_emails=True)
    text_recipients = CustomUser.objects.filter(receives_text_alerts=True)

    # Load in alarms from db that need to be processed
    unprocessed_alarms = PLCAlarm.objects.filter(is_active=True, receives_alerts=True)

    tags_to_email: List[str] = []
    for alarm in unprocessed_alarms:
        if alarm.email_sent is False:
            tags_to_email.append(
                f'{alarm.description} ({alarm.tag_name}) - {alarm.timestamp.strftime("%m/%d/%Y %H:%M:%S")}'
            )

    # Get email reset counter
    gen_conf = GeneralConfig.objects.order_by('id').last()
    email_reset_minutes = gen_conf.email_reset_minutes

    if len(tags_to_email) > 0:
        gmail_user = settings.GMAIL_USER
        gmail_password = settings.GMAIL_PASSWORD

        email_from: str = gmail_user
        email_to: List[str] = []

        for recipient in email_recipients:
            email_to.append(recipient.email)

        for recipient in text_recipients:
            if recipient.receives_text_alerts is True and (recipient.text_to_address is not None
                                                           or recipient.text_to_address != ''):
                email_to.append(recipient.text_to_address)

        email_body: MIMEMultipart = MIMEMultipart('alternative')
        email_body['Subject'] = 'IST Grenada PLC Alert'
        email_body['From'] = gmail_user

        email_text = f"""
The following PLC tags have triggered an alarm:
{os.linesep.join(tags_to_email)}

NOTE: This is an automated email. Please do not reply.
"""

        email_body.attach(MIMEText(email_text, 'plain'))

        try:
            if dry_run is False:
                # print('Sending email...')
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_password)
                server.sendmail(email_from, email_to, email_body.as_string())
                server.close()
                # print('Email sent.')
            else:
                print(email_text)
        except Exception as ex:
            print(ex)

    for alarm in unprocessed_alarms:
        if alarm.email_sent is False:
            alarm.email_sent = True

        if alarm.email_sent_counter < email_reset_minutes:
            alarm.email_sent_counter += 1
        else:
            alarm.email_sent_counter = 1
            alarm.email_sent = False

    PLCAlarm.objects.bulk_update(unprocessed_alarms, ['email_sent', 'email_sent_counter', ])
