import asyncio
import logging
from asyncio import Protocol, Transport, Future
import random
from os import getenv

from main import ConnectPacket, PingPacket, PublishPacket, SubsribePacket, control_field_to_str, vbi_decode 
from tg import bot
from q import shared_queue, Message, Direction, MessageType, SMSData
from at import AT, ATReplyManage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('pmqtt')
at = AT()
at_rm = ATReplyManage()

KA_TIMEOUT = 60
CHAT_ID = getenv('CHAT_ID')


def publish(topic: str, message: str, transport: Transport):
    packet = PublishPacket(topic=topic, payload=message)
    if transport:
        transport.write(packet.to_bytes())

future_waits = {} 



async def handle_queue(transport):
    while True:
        message: Message = await shared_queue.get()
        logger.debug(f'message: {message}')
        if message.direction == Direction.MQTT:
            if message.message_type == MessageType.SMS:
                wait_for_reply = Future()
                future_waits['sms'] = wait_for_reply
                if isinstance(message.message, SMSData):
                    sms_data: SMSData = message.message
                    asyncio.create_task(at.send_message(sms_data.message, sms_data.number, publish, transport, wait_for_reply))
            elif message.message_type == MessageType.LOCATION:
                asyncio.create_task(at.get_location(message.message, publish, transport))
            else:
                if isinstance(message.message, str):
                    publish('input', message.message, transport)
        elif message.direction == Direction.TG:
            try:
                if isinstance(message.message, str):
                    if message.message.startswith('OK') and message.message.endswith('>') or message.message == '>':
                        future_waits['sms'].set_result(True)
                        del future_waits['sms']
                        continue
                    elif at_rm.handle_message(message.message, bot):
                        continue
                    elif message.message != '':
                        logger.debug(f'Sending TG message: {message.message}')
                        asyncio.create_task(bot.send_message(chat_id=CHAT_ID, text=message.message))
            except Exception as e:
                logger.error(f'Error sending TG message: {e}')


class MqttProtocol(Protocol):

    def __init__(self, conn_lost):
        self.transport = None
        self.conn_lost = conn_lost

    def connection_made(self, transport: Transport) -> None:
        logger.debug('Connection made')
        self.transport = transport
        packet = ConnectPacket(
            version=5,  keepalive=KA_TIMEOUT, client_id='test').to_bytes()
        transport.write(packet)

    def connection_lost(self, exc: Exception | None) -> None:
        logger.debug('Connection lost')
        self.conn_lost.set_result(True)

    def data_received(self, data: bytes) -> None:
        try:
            control_byte = data[0:1]

            if control_byte == b'':
                logger.debug('Connection closed')
                self.conn_lost.set_result(True)

            packet_type = control_field_to_str(control_byte[0])
            length, bytes_consumed = vbi_decode(data[1:])
            packet = data[1+bytes_consumed:]

            logger.info(f'Received: { packet_type }')

            if packet_type == 'PUBLISH':
                parsed = PublishPacket.parse(packet)
                logger.debug(f'Parsed packet: { parsed.payload }')
                shared_queue.put_nowait(Message(parsed.payload, Direction.TG))

            elif packet_type == 'CONNACK':
                asyncio.get_event_loop().call_later(10, self.send_ping)
                logger.debug('Connection accepted, subscribing to input topic')
                self.subscribe('output')
        except Exception as e:
            logger.error(f'Error parsing packet: {e}')

    def subscribe(self, topic: str):
        packet = SubsribePacket(
            topic=topic, packet_id=random.randint(0, 255), qos=0).to_bytes()
        if self.transport:
            self.transport.write(packet)

    def send_ping(self):
        packet = PingPacket().to_bytes()
        if self.transport:
            self.transport.write(packet)
        asyncio.get_event_loop().call_later(KA_TIMEOUT - 20, self.send_ping)


async def connect():
    loop = asyncio.get_event_loop()
    conn_lost = loop.create_future()
    transport, protocol = await loop.create_connection(lambda: MqttProtocol(conn_lost), 'localhost', 1883)
    return transport, protocol, conn_lost


async def main():
    conn_lost = Future()

    t2 = asyncio.create_task(connect())
    transport, protocol, conn_lost = await t2
    asyncio.create_task(bot.polling())
    asyncio.create_task(handle_queue(transport))

    try:
        await conn_lost
    finally:
        transport.close()

asyncio.run(main())
