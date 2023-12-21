from asyncio import queues
from enum import Enum
from dataclasses import dataclass
from typing import Union, Literal


class Direction(Enum):
    MQTT = 0
    TG = 1


class MessageType(Enum):
    NONE = 0
    SMS = 1
    LOCATION = 2
    LocationReply = 3
    Error = 4


@dataclass
class SMSData:
    number: str
    message: str


@dataclass
class Message:
    message: Union[str, object]
    direction: Direction
    message_type: MessageType = MessageType.NONE


@dataclass
class SignalStrength:
    sysmode: Literal['NOSERVICE', 'GSM', 'LTE']
    gsm_rssl: str | None = None
    lte_rssi: str | None = None
    lte_rsrp: str | None = None
    lte_sinr: str | None = None
    lte_rsrq: str | None = None

    def __str__(self) -> str:
        if self.sysmode == 'NOSERVICE':
            return 'No service'
        if self.sysmode == 'GSM':
            return f'''Netowrok Type: {self.sysmode}
Strength: {self.gsm_rssl} dBm'''
        return f'''Netowrok Type: {self.sysmode}
Strength: {self.lte_rssi} dBm
Received Power: {self.lte_rsrp} dBm
Signal to Noise Ratio: {self.lte_sinr} dB
Reference Signal Strength: {self.lte_rsrq} dB'''


shared_queue = queues.Queue()
