import asyncio
import json
import logging
from q import shared_queue, Message, Direction, MessageType
from errorcodes import ErrorCodes

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    async def handle_location(self, msg: str):
        first_line = msg.split('\n')[0]
        command, location = first_line.split(':')
        utc, lat, lon, hdop, alt, fix, cog, spkm, spkn, date, nsat = location.split(
            ',')
        json_location = {'utc': utc, 'lat': lat, 'lon': lon, 'hdop': hdop, 'alt': alt,
                         'fix': fix, 'cog': cog, 'spkm': spkm, 'spkn': spkn, 'date': date, 'nsat': nsat}
        to_google_maps = f'https://www.google.com/maps/place/{lat},{lon}'
        await shared_queue.put(Message(message=json.dumps(json_location), direction=Direction.TG, message_type=MessageType.LocationReply))
        await shared_queue.put(Message(message=to_google_maps, direction=Direction.TG, message_type=MessageType.LocationReply))


    async def handle_errors(self, msg: str):
        error_code = msg.split(':')[1].strip()
        error_message = ErrorCodes.get(int(error_code), 'Unknown error')
        await shared_queue.put(Message(message=f'Error: {error_message}', direction=Direction.TG, message_type=MessageType.NONE))
