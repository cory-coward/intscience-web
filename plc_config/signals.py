from django.core.cache import cache
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from typing import List, Tuple

from plc_config.models import WellConfig
from plc_core.plc_core import PlcCore, PlcResponse


@receiver(pre_save, sender=WellConfig)
def get_well_cycle_gallons_sleep_minutes(sender, instance, **kwargs):
    # If this is a new object, get values from PLC
    if instance.pk is None:
        tag: str = instance.tag_prefix

        tags_to_read: List[str] = [f'{tag}.CycleGallons_SP', f'{tag}.SleepMinutes_SP']

        plc_ip_address: str = settings.PLC_IP
        plc: PlcCore = PlcCore(plc_ip_address)

        tags_response: PlcResponse = plc.read_list_of_tags(tags_to_read)

        plc_read_success: bool = True

        for r in tags_response:
            print(f'{r.TagName}: {r.Value}, {r.Status}')
            if r.Status != 'Success':
                plc_read_success = False
                break

        if plc_read_success:
            instance.cycle_gallons = [x for x in tags_response if x.TagName == f'{tag}.CycleGallons_SP'][0].Value
            instance.sleep_minutes = [x for x in tags_response if x.TagName == f'{tag}.SleepMinutes_SP'][0].Value


@receiver(post_save, sender=WellConfig)
def set_well_cycle_gallons_sleep_minutes(sender, instance, created, **kwargs) -> bool:
    # If this object is new, skip
    if created:
        return True

    tag: str = instance.tag_prefix
    cycle_gallons: int = instance.cycle_gallons
    sleep_minutes: int = instance.sleep_minutes

    plc_ip_address: str = settings.PLC_IP
    data: List[Tuple[str, any]] = [(f'{tag}.CycleGallons_SP', cycle_gallons),
                                   (f'{tag}.SleepMinutes_SP', sleep_minutes)]

    plc: PlcCore = PlcCore(plc_ip_address)
    response: PlcResponse = plc.write_tag_list(data)

    write_success: bool = True

    for r in response:
        print(f'{r.TagName}: {r.Status}')
        if r.Status != 'Success':
            write_success = False
            break

    return write_success


@receiver(post_save, sender=WellConfig)
def reset_well_period_cache(sender, instance, **kwargs):
    cache.set(settings.CACHE_KEY_WELL_READINGS_COUNT, 1, None)
