from dataclasses import dataclass
from datetime import datetime


@dataclass
class PlcWellItem:
    source_tag: str = ''
    pump_mode: str = ''
    is_running: bool = False
    flow_rate: float = 0.0
    flow_total: float = 0.0


@dataclass
class PlcAirStripperItem:
    source_tag: str = ''
    pump_runtime: float = 0.0
    blower_runtime: float = 0.0


@dataclass
class PlcZoneFlowItem:
    zone_flow_right: float = 0.0
    zone_flow_left: float = 0.0


@dataclass
class PlcGardnerDenverItem:
    intake_pre_air_filter_vacuum: float = 0.0
    intake_temp: float = 0.0


@dataclass
class PlcHeatExchangerItem:
    flow_rate: float = 0.0
    flow_total: float = 0.0
    pressure: float = 0.0
    outlet_air_temp: float = 0.0


@dataclass
class PlcSurgeTankItem:
    flow_rate: float = 0.0
    flow_total: float = 0.0


@dataclass
class PlcDischargeWaterItem:
    flow_rate: float = 0.0
    flow_total: float = 0.0


@dataclass
class PlcAlarmItem:
    alarm_tag: str = ''
    alarm_description: str = ''
    dial: bool = False
    alarm_time: datetime = datetime.now
    ack_time: datetime = datetime.now
    clear_time: datetime = datetime.now
    alarm_active: bool = False
