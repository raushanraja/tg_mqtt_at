from asyncio import queues
from enum import Enum
from dataclasses import dataclass
from typing import Union


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


shared_queue = queues.Queue()
