import pytz
import time

from datetime import datetime
from decimal import Decimal
from typing import List

from django.conf import settings
from django.core.cache import cache

from plc_config.models import GeneralConfig, WellConfig, AirStripperConfig
from plc_logs.models import WellLogEntry, AirStripperLogEntry, ZoneFlowLogEntry, GardnerDenverBlowerLogEntry, \
    HeatExchangerLogEntry

from .plc_alarms import process_alarms
from .plc_core import PlcCore, PlcResponse
from .plc_items import PlcWellItem, PlcAirStripperItem, PlcZoneFlowItem, PlcGardnerDenverItem, PlcHeatExchangerItem


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

    # Create empty items/lists of plc items
    plc_well_items: List[PlcWellItem] = []
    plc_air_stripper_items: List[PlcAirStripperItem] = []
    plc_zone_flow_item: PlcZoneFlowItem = PlcZoneFlowItem()
    plc_gardner_denver_item: PlcGardnerDenverItem = PlcGardnerDenverItem()
    plc_heat_exchanger_item: PlcHeatExchangerItem = PlcHeatExchangerItem()

    # Configure list of tags to read
    tags_to_read: List[str] = []

    plc_datetime_format = '%m/%d/%Y %H:%M:%S'
    ctz = pytz.timezone('America/Chicago')

    # Well tags
    for well in wells:
        tags_to_read.append(f'{well.tag_prefix}.AutoMode')
        tags_to_read.append(f'{well.tag_prefix}.Running')
        tags_to_read.append(f'{well.tag_prefix}.FlowRate')
        tags_to_read.append(f'{well.tag_prefix}.FlowTotal')

    # Air stripper tags
    for air_str in air_strippers:
        tags_to_read.append(f'{air_str.tag_prefix}.Pump.Runtime')
        tags_to_read.append(f'{air_str.tag_prefix}.Blower.Runtime')

    # Zone flow tags
    tags_to_read.append('Zone_Flow_Right')
    tags_to_read.append('Zone_Flow_Left')

    # Gardner Denver tags
    tags_to_read.append('GD_Blower.IntakePreAirFilterVacuum')
    tags_to_read.append('GD_Blower.IntakeTemperature')

    # Heat exchanger tags
    tags_to_read.append('HeatExchanger.FlowRate')
    tags_to_read.append('HeatExchanger.FlowTotal')
    tags_to_read.append('HeatExchanger.Pressure')
    tags_to_read.append('HeatExchanger.OutletAirTemp')

    # Read list of tags
    plc = PlcCore(ip_address=settings.PLC_IP)
    tags_response: PlcResponse = plc.read_list_of_tags(tags_to_read)

    # Cycle through tags and sort into plcitem list
    # Wells
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

    # Air strippers
    for air_stripper in air_strippers:
        related_tags = [res for res in tags_response if res.TagName.startswith(air_stripper.tag_prefix)]

        air_stripper_item = PlcAirStripperItem()
        air_stripper_item.source_tag = air_stripper.tag_prefix
        air_stripper_item.pump_runtime = [x for x in related_tags if x.TagName.endswith('Pump.Runtime')][0].Value
        air_stripper_item.blower_runtime = [x for x in related_tags if x.TagName.endswith('Blower.Runtime')][0].Value

        plc_air_stripper_items.append(air_stripper_item)

    # Zone flow
    zone_flow_related_tags = [x for x in tags_response if x.TagName.startswith('Zone_Flow_')]
    plc_zone_flow_item.zone_flow_left = [x for x in zone_flow_related_tags if x.TagName.endswith('Left')][0].Value
    plc_zone_flow_item.zone_flow_right = [x for x in zone_flow_related_tags if x.TagName.endswith('Right')][0].Value

    # Gardner Denver
    gardner_denver_related_tags = [x for x in tags_response if x.TagName.startswith('GD_Blower')]
    plc_gardner_denver_item.intake_pre_air_filter_vacuum = [x for x in gardner_denver_related_tags
                                                            if x.TagName.endswith('IntakePreAirFilterVacuum')][0].Value
    plc_gardner_denver_item.intake_temp = [x for x in gardner_denver_related_tags
                                           if x.TagName.endswith('IntakeTemperature')][0].Value

    # Heat exchanger
    heat_exchanger_related_tags = [x for x in tags_response if x.TagName.startswith('HeatExchanger')]
    plc_heat_exchanger_item.flow_rate = [x for x in heat_exchanger_related_tags
                                         if x.TagName.endswith('FlowRate')][0].Value
    plc_heat_exchanger_item.flow_total = [x for x in heat_exchanger_related_tags
                                          if x.TagName.endswith('FlowTotal')][0].Value
    plc_heat_exchanger_item.pressure = [x for x in heat_exchanger_related_tags
                                        if x.TagName.endswith('Pressure')][0].Value
    plc_heat_exchanger_item.outlet_air_temp = [x for x in heat_exchanger_related_tags
                                               if x.TagName.endswith('OutletAirTemp')][0].Value

    # Check if we need to add well measurements to db
    print(f'PLC readings count: {plc_readings_count}')
    print(f'PLC record time: {well_record_time}')
    if ignore_period is True or (plc_readings_count * 15 == well_record_time * 60):
        # Save to db and reset record_counter
        print('Saving to db')

        well_db_objects: List[WellLogEntry] = []
        air_stripper_db_objects: List[AirStripperLogEntry] = []

        # Well items
        for well_item in plc_well_items:
            log_entry = WellLogEntry()
            log_entry.well_name = well_item.source_tag
            log_entry.gal_per_minute = Decimal(well_item.flow_rate)
            log_entry.total_gal = Decimal(well_item.flow_total)
            log_entry.pump_mode = WellLogEntry.AUTO if well_item.pump_mode == 'Auto' else WellLogEntry.MANUAL
            log_entry.is_running = well_item.is_running

            well_db_objects.append(log_entry)

        # Air stripper items
        for air_stripper_item in plc_air_stripper_items:
            log_entry = AirStripperLogEntry()
            log_entry.air_stripper_name = air_stripper_item.source_tag
            log_entry.pump_runtime = air_stripper_item.pump_runtime
            log_entry.blower_runtime = air_stripper_item.blower_runtime

            air_stripper_db_objects.append(log_entry)

        # Gardner Denver items
        gd_log_entry = GardnerDenverBlowerLogEntry()
        gd_log_entry.intake_pre_air_filter_vacuum = plc_gardner_denver_item.intake_pre_air_filter_vacuum
        gd_log_entry.intake_temp = plc_gardner_denver_item.intake_temp

        # Zone flow items
        zone_flow_log_entry = ZoneFlowLogEntry()
        zone_flow_log_entry.zone_flow_left = plc_zone_flow_item.zone_flow_left
        zone_flow_log_entry.zone_flow_right = plc_zone_flow_item.zone_flow_right

        # Heat exchanger items
        heat_exchanger_log_entry = HeatExchangerLogEntry()
        heat_exchanger_log_entry.flow_rate = plc_heat_exchanger_item.flow_rate
        heat_exchanger_log_entry.flow_total = plc_heat_exchanger_item.flow_total
        heat_exchanger_log_entry.pressure = plc_heat_exchanger_item.pressure
        heat_exchanger_log_entry.outlet_air_temp = plc_heat_exchanger_item.outlet_air_temp

        WellLogEntry.objects.bulk_create(well_db_objects)
        AirStripperLogEntry.objects.bulk_create(air_stripper_db_objects)
        gd_log_entry.save()
        zone_flow_log_entry.save()
        heat_exchanger_log_entry.save()

        cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
    else:
        # Increment record_counter
        cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, plc_readings_count + 1, None)

    # Save well readings to cache
    well_cache_objects = []
    air_stripper_cache_objects = []
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

    for air_stripper_item in plc_air_stripper_items:
        air_str_c = {
            'air_stripper_name': air_stripper_item.source_tag,
            'pump_runtime': air_stripper_item.pump_runtime,
            'blower_runtime': air_stripper_item.blower_runtime,
            'timestamp': datetime.now(ctz)
        }
        air_stripper_cache_objects.append(air_str_c)

    zone_flow_c = {
        'zone_flow_left': plc_zone_flow_item.zone_flow_left,
        'zone_flow_right': plc_zone_flow_item.zone_flow_right,
    }

    gardner_denver_c = {
        'intake_pre_air_filter_vacuum': plc_gardner_denver_item.intake_pre_air_filter_vacuum,
        'intake_temp': plc_gardner_denver_item.intake_temp,
    }

    heat_exchanger_c = {
        'flow_rate': plc_heat_exchanger_item.flow_rate,
        'flow_total': plc_heat_exchanger_item.flow_total,
        'pressure': plc_heat_exchanger_item.pressure,
        'outlet_air_temp': plc_heat_exchanger_item.outlet_air_temp,
    }

    cache.set(settings.CACHE_KEY_CURRENT_WELL_READINGS, well_cache_objects, None)
    cache.set(settings.CACHE_KEY_CURRENT_AIR_STRIPPER_READINGS, air_stripper_cache_objects, None)
    cache.set(settings.CACHE_KEY_CURRENT_ZONE_FLOW_READINGS, zone_flow_c, None)
    cache.set(settings.CACHE_KEY_CURRENT_GARDNER_DENVER_READINGS, gardner_denver_c, None)
    cache.set(settings.CACHE_KEY_CURRENT_HEAT_EXCHANGER_READINGS, heat_exchanger_c, None)

    # Process alarms
    process_alarms()

    end = time.time()
    print(f'Time elapsed: {(end-start) * 10**3}ms')


def set_well_mode(well_name: str, new_mode: str) -> bool:
    tag_name = f'{well_name}.AutoMode'

    new_mode = True if new_mode == 'Auto' else False

    plc = PlcCore(ip_address=settings.PLC_IP)
    plc_response = plc.write_tag(tag_name, new_mode)

    return plc_response.Status == 'Success'
