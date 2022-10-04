import pytz
import time

from datetime import datetime
from typing import List

from django.conf import settings
from django.core.cache import cache

from plc_config.models import GeneralConfig, WellConfig
from plc_logs.models import WellLogEntry

from .plc_alarms import PlcAlarms
from .plc_core import PlcCore, PlcResponse
from .plc_item import PLCItem


class PlcMeasurements:
    @staticmethod
    def read_wells():
        start = time.time()

        # Load in time between data records
        gen_config = GeneralConfig.objects.order_by('-id').first()
        well_record_time = gen_config.well_record_minutes if gen_config is not None else 60

        # Load in wells from db
        wells = WellConfig.objects.all()

        # Load in well_readings_count from cache
        count_from_cache = cache.get(settings.CACHE_KEY_WELL_READINGS_COUNT)
        if count_from_cache is None:
            cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
            well_readings_count = 1
        else:
            well_readings_count = count_from_cache

        # Create empty list of plc items
        plc_items: List[PLCItem] = []

        # Configure list of tags to read based on wells from db
        tags_to_read: List[str] = []

        plc_datetime_format = '%m/%d/%Y %H:%M:%S'
        ctz = pytz.timezone('America/Chicago')

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
            item.alarm_active = [x for x in related_tags if x.TagName.endswith('Active')][0].Value
            item.alarm_count = [x for x in related_tags if x.TagName.endswith('Count')][0].Value

            item.alarm_time = None
            item.ack_time = None
            item.clear_time = None

            if raw_alarm_time != '' and raw_alarm_time is not None:
                item.alarm_time = datetime.strptime(raw_alarm_time, plc_datetime_format).replace(tzinfo=ctz)

            if raw_ack_time != '' and raw_ack_time is not None:
                item.ack_time = datetime.strptime(raw_ack_time, plc_datetime_format).replace(tzinfo=ctz)

            if raw_clear_time != '' and raw_clear_time is not None:
                item.clear_time = datetime.strptime(raw_clear_time, plc_datetime_format).replace(tzinfo=ctz)

            plc_items.append(item)

        PlcAlarms.process_alarms(plc_items)

        # Check if we need to add well measurements to db
        if well_readings_count * 10 == well_record_time * 60:
            # Save to db and reset record_counter
            well_db_objects: List[WellLogEntry] = []

            for item in plc_items:
                log_entry = WellLogEntry()
                log_entry.well_name = item.source_tag
                log_entry.gal_per_minute = item.flow_rate
                log_entry.total_gal = item.flow_total
                log_entry.is_running = item.is_running

                well_db_objects.append(log_entry)

            WellLogEntry.objects.bulk_create(well_db_objects)
            cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
        else:
            # Increment record_counter
            cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, well_readings_count + 1, None)

        # Save well readings to cache
        well_cache_objects = []
        for item in plc_items:
            wc = {
                'well_name': item.source_tag,
                'gal_per_minute': item.flow_rate,
                'total_gal': item.flow_total,
                'is_running': item.is_running,
                'timestamp': datetime.now(ctz)
            }
            well_cache_objects.append(wc)

        cache.set(settings.CACHE_KEY_CURRENT_WELL_READINGS, well_cache_objects, None)

        end = time.time()
        print(f'Time elapsed: {(end-start) * 10**3}ms')

        # return plc_items
