# Desc: Telegram reply manager
# Date: 2021-04-25
# Author: raushanraja

from dataclasses import dataclass
from typing import Dict, List, Union, Tuple
from enum import Enum

from telebot.async_telebot import types
from q import Message, Direction, MessageType, shared_queue, SMSData
import logging

logger = logging.getLogger(__name__)


class ReplyManageType(Enum):
    NONE = 0
    SMSNUMBER = 1
    SMSTEXT = 2




class ReplyHander:

    def __init__(self, replymanager: 'ReplyManager', bot) -> None:
        self.rm = replymanager
        self.bot = bot

    async def handle_sms_number(self, message, reply) -> Union[str, None]:
        number = message.text

        if number.isnumeric() and len(number) == 10:
            number = '+91' + number
        elif number.startswith('+') and number[1:].isnumeric() and len(number) == 13:
            pass
        else:
            await self.bot.send_message(message.chat.id, "Invalid number")
            return

        markup = types.ForceReply(selective=False)
        sent_message = await self.bot.send_message(message.chat.id, "Enter the message to send as SMS", reply_markup=markup)
        self.rm.add(ReplyData(message.chat.id, sent_message.id, ReplyManageType.SMSTEXT))
        self.rm.remove(reply)
        self.rm.reply_data[sent_message.id] = SMSData(number=number, message='')

    async def handle_sms_text(self, message, reply) -> Union[str, None]:
        reply_data = self.rm.reply_data.get(reply.message_id)
        if reply_data:
            reply_data.message = message.text
            self.rm.remove(reply)
            logger.debug(f"Sending SMS {reply_data}")
            await shared_queue.put(Message(message=reply_data, direction=Direction.MQTT, message_type=MessageType.SMS))
    


class ReplyData:
    def __init__(self, chat_id: Union[int, str], message_id: Union[int, str], manage_type: ReplyManageType) -> None:
        self.chat_id = chat_id
        self.message_id = message_id
        self.manage_type = manage_type

    
    def __hash__(self) -> int:
        return hash((self.chat_id, self.message_id, self.manage_type))

    def __eq__(self, o: 'ReplyData') -> bool:
        return self.chat_id == o.chat_id and self.message_id == o.message_id and self.manage_type == o.manage_type

    def __contains__(self, o: 'ReplyData') -> bool:
        return self.__eq__(o)

    def __repr__(self) -> str:
        return f'ReplyData(chat_id={self.chat_id}, message_id={self.message_id}, manage_type={self.manage_type})'


class ReplyManager:

    def __init__(self, bot) -> None:
        self.replies: Dict[Tuple[Union[int, str], Union[int, str]], ReplyData] = {}
        self.reply_data = {}
        self.handler = ReplyHander(self, bot)

    def add(self, reply_data: ReplyData) -> None:
        self.replies[(reply_data.chat_id, reply_data.message_id)] = reply_data

    def remove(self, reply_data: ReplyData) -> None:
        if reply_data in self.replies:
            del self.replies[(reply_data.chat_id, reply_data.message_id)]

    async def handle_reply(self, chat_id, message_id , message) -> None:
           reply= self.replies.get((chat_id, message_id))
           logger.debug(f"Reply data {reply}")
           if reply:
               if reply.manage_type == ReplyManageType.SMSNUMBER:
                    await self.handler.handle_sms_number(message, reply)
               elif reply.manage_type == ReplyManageType.SMSTEXT:
                    await self.handler.handle_sms_text(message, reply)
