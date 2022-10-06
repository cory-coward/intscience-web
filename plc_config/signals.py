from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from plc_config.models import WellConfig
from plc_core.plc_core import PlcCore, PlcResponse


@receiver(post_save, sender=WellConfig)
def set_well_cycle_gallons_sleep_minutes(sender, instance, **kwargs) -> bool:
    tag: str = instance.tag_prefix
    cycle_gallons: int = instance.cycle_gallons
    sleep_minutes: int = instance.sleep_minutes

    print(f'{tag} cycle gallons: {cycle_gallons}')
    print(f'{tag} sleep minutes: {sleep_minutes}')

    plc_ip_address: str = settings.PLC_IP
    plc: PlcCore = PlcCore(plc_ip_address)

    response: PlcResponse = plc.write_tag(f'{tag}.CycleGallons_SP', cycle_gallons)

    print(response.Status)

    return response.Status == 'Success'
