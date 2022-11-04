from dataclasses import dataclass
from datetime import datetime


@dataclass
class PlcWellItem:
    source_tag: str = ''
    pump_mode: str = ''
    is_running: bool = False
    flow_rate: float = 0.0
    flow_total: float = 0.0
    # dial: bool = False
    # alarm_time: datetime = datetime.now
    # ack_time: datetime = datetime.now
    # clear_time: datetime = datetime.now
    # alarm_active: bool = False
    # alarm_count: int = 0


@dataclass
class PlcAirStripperItem:
    source_tag: str = ''


@dataclass
class PlcAlarmItem:
    alarm_tag: str = ''
    alarm_description: str = ''
    dial: bool = False
    alarm_time: datetime = datetime.now
    ack_time: datetime = datetime.now
    clear_time: datetime = datetime.now
    alarm_active: bool = False