import asyncio
from os import getenv
import json
import logging

from telebot.async_telebot import AsyncTeleBot
from q import shared_queue, Message, Direction, MessageType
from errorcodes import ErrorCodes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


CHAT_ID = getenv('CHAT_ID')

if not CHAT_ID:
    raise Exception('CHAT_ID not set in env')


class AT:

    async def send_message(self, message: str, number: str, publish, transport, wait_for_reply):
        # Change the Mode to Text Mode
        end_of_sms = 'EOSS'
        topic = 'input'
        m = 'AT+CMGF=1'
        publish(topic, m, transport)
        # Set the GSM Module in Text Mode
        m = 'AT+CMGS="' + number + '"'
        publish(topic, m, transport)
        # Wait for the '>' character
        await wait_for_reply

        # Send a message to a particular Number
        publish(topic, message, transport)
        publish(topic, end_of_sms, transport)

    async def get_location(self, message, publish, transport):
        topic = 'input'
        if message == 'get':
            m = 'AT+QGPSLOC=2'
        elif message == 'stop':
            m = 'AT+QGPSEND'
        elif message == 'start':
            m = 'AT+QGPS=1'
        else:
            m = 'AT+QGPSLOC=2'
        publish(topic, m, transport)


class ATReplyManage:

    method_map = {
        '+CMTI:': 'read_message',
        '+QGPSLOC:': 'handle_location',
        '+CMS ERROR:': 'handle_errors'
    }

    def handle_message(self, msg: str, bot: AsyncTeleBot):
        for key in self.method_map.keys():
            if msg.startswith(key):
                method = getattr(self, self.method_map[key])
                asyncio.create_task(method(msg, bot))
                return True
        return False

    async def handle_location(self, msg: str, bot: AsyncTeleBot):
        first_line = msg.split('\n')[0]
        command, location = first_line.split(':')
        utc, lat, lon, hdop, alt, fix, cog, spkm, spkn, date, nsat = location.split(
            ',')
        json_location = {'utc': utc, 'lat': lat, 'lon': lon, 'hdop': hdop, 'alt': alt,
                         'fix': fix, 'cog': cog, 'spkm': spkm, 'spkn': spkn, 'date': date, 'nsat': nsat}
        to_google_maps = f'https://www.google.com/maps/place/{lat},{lon}'
        if CHAT_ID and bot:
            try:
                await bot.send_message(CHAT_ID, json.dumps(json_location))
                await bot.send_message(CHAT_ID, to_google_maps)
                await bot.send_location(CHAT_ID, float(lat), float(lon))
            except Exception as e:
                logger.error(f'Error sending location message: {e}')

    async def handle_errors(self, msg: str, bot: AsyncTeleBot):
        error_code = msg.split(':')[1].strip()
        error_message = ErrorCodes.get(int(error_code), 'Unknown error')
        if CHAT_ID and bot:
            try:
                await bot.send_message(CHAT_ID, f'Error: {error_message}')
            except Exception as e:
                logger.error(f'Error sending error message: {e}')

    async def read_message(self, msg: str, bot: AsyncTeleBot):
        command, new_message = msg.split(':')
        index = new_message.strip().split(',')[1].strip()
        await shared_queue.put(Message(message=f'AT+CMGR={index}', direction=Direction.MQTT, message_type=MessageType.NONE))
