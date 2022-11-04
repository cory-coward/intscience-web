import pytz
import time

from datetime import datetime
from decimal import Decimal
from typing import List

from django.conf import settings
from django.core.cache import cache

from plc_config.models import GeneralConfig, WellConfig, AirStripperConfig
from plc_logs.models import WellLogEntry, AirStripperLogEntry

from .plc_alarms import process_alarms
from .plc_core import PlcCore, PlcResponse
from .plc_items import PlcWellItem, PlcAirStripperItem


def read_plc_tags(ignore_period: bool = False):
    start = time.time()

    # Load in time between data records
    gen_config = GeneralConfig.objects.order_by('-id').first()
    well_record_time = gen_config.well_record_minutes if gen_config is not None else 60

    # Load in plc items from db
    wells = WellConfig.objects.all()
    air_strippers = AirStripperConfig.objects.all()
    # num_wells = WellConfig.objects.count()
    # num_air_strippers = AirStripperConfig.objects.count()

    # Load in plc_readings_count from cache
    count_from_cache = cache.get(settings.CACHE_KEY_WELL_READINGS_COUNT)
    if count_from_cache is None:
        cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
        plc_readings_count = 1
    else:
        plc_readings_count = count_from_cache

    # Create empty lists of plc items
    plc_well_items: List[PlcWellItem] = []
    plc_air_stripper_items: List[PlcAirStripperItem] = []

    # Configure list of tags to read based on wells from db
    tags_to_read: List[str] = []

    plc_datetime_format = '%m/%d/%Y %H:%M:%S'
    ctz = pytz.timezone('America/Chicago')

    for well in wells:
        tags_to_read.append(f'{well.tag_prefix}.AutoMode')
        tags_to_read.append(f'{well.tag_prefix}.Running')
        tags_to_read.append(f'{well.tag_prefix}.FlowRate')
        tags_to_read.append(f'{well.tag_prefix}.FlowTotal')

    for air_str in air_strippers:
        tags_to_read.append(f'{air_str.tag_prefix}.Pump.Runtime')
        tags_to_read.append(f'{air_str.tag_prefix}.Blower.Runtime')

    # Read list of tags
    plc = PlcCore(ip_address=settings.PLC_IP)
    tags_response: PlcResponse = plc.read_list_of_tags(tags_to_read)

    # Cycle through tags and sort into plcitem list
    for well in wells:
        related_tags = [res for res in tags_response if res.TagName.startswith(well.tag_prefix)]

        well_item = PlcWellItem()
        well_item.source_tag = well.tag_prefix
        well_item.pump_mode = 'Auto' if [x for x in related_tags if x.TagName.endswith('AutoMode')][0].Value is True \
            else 'Manual'
        well_item.is_running = [x for x in related_tags if x.TagName.endswith('Running')][0].Value
        well_item.flow_rate = [x for x in related_tags if x.TagName.endswith('FlowRate')][0].Value
        well_item.flow_total = [x for x in related_tags if x.TagName.endswith('FlowTotal')][0].Value

        plc_well_items.append(well_item)

    for air_stripper in air_strippers:
        related_tags = [res for res in tags_response if res.TagName.startswith(air_stripper.tag_prefix)]

        air_stripper_item = PlcAirStripperItem()
        air_stripper_item.source_tag = air_stripper.tag_prefix
        air_stripper_item.pump_runtime = [x for x in related_tags if x.TagName.endswith('Pump.Runtime')][0].Value
        air_stripper_item.blower_runtime = [x for x in related_tags if x.TagName.endswith('Blower.Runtime')][0].Value

        plc_air_stripper_items.append(air_stripper_item)

    # Check if we need to add well measurements to db
    print(f'PLC readings count: {plc_readings_count}')
    print(f'PLC record time: {well_record_time}')
    if ignore_period is True or (plc_readings_count * 15 == well_record_time * 60):
        # Save to db and reset record_counter
        print('Saving to db')

        well_db_objects: List[WellLogEntry] = []
        air_stripper_db_objects: List[AirStripperLogEntry] = []

        for well_item in plc_well_items:
            log_entry = WellLogEntry()
            log_entry.well_name = well_item.source_tag
            log_entry.gal_per_minute = Decimal(well_item.flow_rate)
            log_entry.total_gal = Decimal(well_item.flow_total)
            log_entry.pump_mode = WellLogEntry.AUTO if well_item.pump_mode == 'Auto' else WellLogEntry.MANUAL
            log_entry.is_running = well_item.is_running

            well_db_objects.append(log_entry)

        for air_stripper_item in plc_air_stripper_items:
            log_entry = AirStripperLogEntry()
            log_entry.air_stripper_name = air_stripper_item.source_tag
            log_entry.pump_runtime = air_stripper_item.pump_runtime
            log_entry.blower_runtime = air_stripper_item.blower_runtime

            air_stripper_db_objects.append(log_entry)

        WellLogEntry.objects.bulk_create(well_db_objects)
        AirStripperLogEntry.objects.bulk_create(air_stripper_db_objects)
        cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
    else:
        # Increment record_counter
        cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, plc_readings_count + 1, None)

    # Save well readings to cache
    well_cache_objects = []
    for well_item in plc_well_items:
        wc = {
            'well_name': well_item.source_tag,
            'gal_per_minute': well_item.flow_rate,
            'total_gal': well_item.flow_total,
            'pump_mode': well_item.pump_mode,
            'is_running': well_item.is_running,
            'timestamp': datetime.now(ctz)
        }
        well_cache_objects.append(wc)

    cache.set(settings.CACHE_KEY_CURRENT_WELL_READINGS, well_cache_objects, None)

    # Process alarms
    process_alarms()

    end = time.time()
    print(f'Time elapsed: {(end-start) * 10**3}ms')

    # return plc_well_items


def set_well_mode(well_name: str, new_mode: str) -> bool:
    tag_name = f'{well_name}.AutoMode'

    new_mode = True if new_mode == 'Auto' else False

    plc = PlcCore(ip_address=settings.PLC_IP)
    plc_response = plc.write_tag(tag_name, new_mode)

    return plc_response.Status == 'Success'
