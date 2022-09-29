import pytz
from dataclasses import dataclass
from datetime import datetime
from typing import List
from django.conf import settings

from plc_alarms.models import PLCAlarm
from plc_config.models import GeneralConfig, WellConfig
from plc_logs.models import WellLogEntry

from .plc_core import PlcCore, PlcResponse

import time


@dataclass
class PLCItem:
    source_tag: str = ''
    is_running: bool = False
    flow_rate: float = 0.0
    flow_total: float = 0.0
    dial: bool = False
    alarm_time: datetime = datetime.now
    ack_time: datetime = datetime.now
    clear_time: datetime = datetime.now
    alarm_active: bool = False
    alarm_count: int = 0


class PlcMeasurements:
    record_counter: int = 0

    @staticmethod
    def read_wells() -> List[PLCItem]:
        start = time.time()

        # Load in time between data records
        gen_config = GeneralConfig.objects.order_by('-id').first()
        well_record_time = gen_config.well_record_minutes if gen_config is not None else 60

        # Load in wells from db
        wells = WellConfig.objects.all()

        # Create empty list of plc items
        plc_items: List[PLCItem] = []

        # Create empty list of alarm db objects
        current_alarms: List[PLCAlarm] = []

        # Configure list of tags to read based on wells from db
        tags_to_read: List[str] = []

        plc_datetime_format = '%m/%d/%Y %H:%M:%S'

        for well in wells:
            tags_to_read.append(f'{well.tag_prefix}.Running')
            tags_to_read.append(f'{well.tag_prefix}.FlowRate')
            tags_to_read.append(f'{well.tag_prefix}.FlowTotal')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.Dial')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.AlarmTime')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.AckTime')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.ClearTime')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.Control.Active')
            tags_to_read.append(f'{well.tag_prefix}.Alarm_NoRun.Control.Count')

        # Read list of tags
        plc = PlcCore(ip_address=settings.PLC_IP)
        tags_response: PlcResponse = plc.read_list_of_tags(tags_to_read)

        # Cycle through tags and sort into plcitem list
        for well in wells:
            related_tags = [res for res in tags_response if res.TagName.startswith(well.tag_prefix)]

            raw_alarm_time = [x for x in related_tags if x.TagName.endswith('AlarmTime')][0].Value
            raw_ack_time = [x for x in related_tags if x.TagName.endswith('AckTime')][0].Value
            raw_clear_time = [x for x in related_tags if x.TagName.endswith('ClearTime')][0].Value

            item = PLCItem()
            item.source_tag = well.tag_prefix
            item.is_running = [x for x in related_tags if x.TagName.endswith('Running')][0].Value
            item.flow_rate = [x for x in related_tags if x.TagName.endswith('FlowRate')][0].Value
            item.flow_total = [x for x in related_tags if x.TagName.endswith('FlowTotal')][0].Value
            item.dial = [x for x in related_tags if x.TagName.endswith('Dial')][0].Value
            item.alarm_time = datetime.strptime(raw_alarm_time, plc_datetime_format)\
                .replace(tzinfo=pytz.timezone('America/Chicago')) if raw_alarm_time != '' else None
            item.ack_time = datetime.strptime(raw_ack_time, plc_datetime_format)\
                .replace(tzinfo=pytz.timezone('America/Chicago')) if raw_ack_time != '' else None
            item.clear_time = datetime.strptime(raw_clear_time, plc_datetime_format)\
                .replace(tzinfo=pytz.timezone('America/Chicago')) if raw_clear_time != '' else None
            item.alarm_active = [x for x in related_tags if x.TagName.endswith('Active')][0].Value
            item.alarm_count = [x for x in related_tags if x.TagName.endswith('Count')][0].Value

            plc_items.append(item)

        # Cycle through tags looking for alarms; if found, add alarm to list of alarm db objects
        items_with_alarms = [x for x in plc_items if x.dial is True]
        for itm in items_with_alarms:
            a = PLCAlarm()
            a.tag_name = itm.source_tag
            a.is_active = itm.alarm_active
            a.timestamp = itm.alarm_time
            a.timestamp_acknowledged = itm.ack_time
            a.timestamp_cleared = itm.clear_time
            a.alarm_count = itm.alarm_count

            current_alarms.append(a)

        # Add all alarm db objects to db
        if len(current_alarms) > 0:
            PLCAlarm.objects.bulk_create(current_alarms)

        # Send alarm email

        # Check if we need to add well measurements to db
        # If true: save to db and reset record_counter
        # If false: increment record_counter
        if PlcMeasurements.record_counter * 10 == well_record_time * 60:
            well_db_objects: List[WellLogEntry] = []

            for item in plc_items:
                log_entry = WellLogEntry()
                log_entry.well_name = item.source_tag
                log_entry.gal_per_minute = item.flow_rate
                log_entry.total_gal = item.flow_total

                well_db_objects.append(log_entry)

            WellLogEntry.objects.bulk_create(well_db_objects)
            PlcMeasurements.record_counter = 1
        else:
            PlcMeasurements.record_counter += 1

        end = time.time()
        print(f'Time elapsed: {(end-start) * 10**3}ms')

        return plc_items
