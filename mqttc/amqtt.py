import asyncio
from asyncio import streams
from main import PUBLISH, ConnectPacket, SubsribePacket, PingPacket, PublishPacket, control_field_to_str
from tg import bot
from q import shared_queue
from os import getenv


writer = None
sub = False

CHAT_ID = getenv('CHAT_ID')


async def publish(topic: str, message: str):
    global writer
    packet = PublishPacket(topic=topic, payload=message)
    if writer:
        writer.write(packet.to_bytes())
        await writer.drain()


async def handle_queue():
    global writer
    while True:
        item = await shared_queue.get()
        await publish('input', item)
#


async def areader(stream: streams.StreamReader):
    global sub
    while True:
        control_byte = await stream.read(1)
        packet_type = control_field_to_str(control_byte[0])
        length_byte = await stream.read(1)
        length = (length_byte[0])
        packet = await stream.read(length)
        
        if packet_type == 'PUBLISH':
            parsed = PublishPacket.parse(packet)
            await bot.send_message(chat_id=CHAT_ID, text=f'{ parsed.topic.decode() }: {parsed.payload}')
        if not sub:
            await subscribe('output')
            sub = True
        if control_byte == b'':
            print('Connection closed')
            if writer:
                writer.close()
                await writer.wait_closed()
                sub = False
            break


async def send_ping():
    global writer
    packet = PingPacket().to_bytes()
    if writer:
        writer.write(packet)
        await writer.drain()
    await asyncio.sleep(40)
    await send_ping()


async def connect():
    global writer
    packet = ConnectPacket(version=5,  keepalive=60, client_id='test')
    if writer:
        writer.write(packet.to_bytes())
        await writer.drain()


async def subscribe(topic: str):
    global writer
    packet = SubsribePacket(topic=topic, packet_id=1, qos=0)
    if writer:
        writer.write(packet.to_bytes())
        await writer.drain()


async def client():
    global writer
    reader, writer = await streams.open_connection('192.168.68.61', 1883)
    asyncio.create_task(areader(reader))
    asyncio.create_task(bot.polling())
    asyncio.create_task(handle_queue())
    await connect()
    await send_ping()


async def main():
    await client()


if __name__ == '__main__':
    asyncio.run(main())
