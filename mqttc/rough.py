import asyncio
from asyncio import StreamReader, StreamWriter
from main import ConnectPacket

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MQTTException(Exception):
    pass


async def read_packet(reader: StreamReader):
    control_byte = await reader.read(1)
    length_byte = await reader.read(1)
    length = (length_byte[0])
    packet = await reader.read(length)
    print(bin(control_byte[0]), packet)


async def write_packet(writer: StreamWriter, packet: bytes, packet_type):
    # Write the packet length
    packet_length = len(packet)
    while True:
        encoded_byte = packet_length % 128
        packet_length //= 128
        if packet_length > 0:
            encoded_byte |= 0x80
        print(encoded_byte, bytes([encoded_byte]))
        packet = bytes([encoded_byte]) + packet
        if packet_length <= 0:
            break
    # # Write the packet
    packet = bytes([packet_type]) + packet
    writer.write(packet)
    await writer.drain()


async def write_connect(writer: StreamWriter):
    packet = ConnectPacket(5, 60, "test", username="asdlkfal;sdksdfasadfaadsfadfafasdfljaldkfjal;sdfjal;sdfj;lasjdfasdfasdlfjasasdfafasdfasdlkfjlkdfjaldfdd").to_bytes()
    writer.write(packet)
    await writer.drain()


async def main():
    reader, writer = await asyncio.open_connection('172.30.0.2', 1883)

    # Send CONNECT
    
    # await write_packet(writer, b'\x00\x04MQTT\x04\x86\x00\x3c\x00\x08client12', CONNECT)
    await write_connect(writer)
    # # Receive CONNACK
    # packet = await read_packet(reader)
    # print(packet)
    # # Send PUBLISH
    # await write_packet(writer, b'\x00\x05topic\x00\x05hello')
    # # Receive PUBACK
    # packet = await read_packet(reader)
    # print(packet)
    # # Send DISCONNECT
    # await write_packet(writer, b'\xe0\x00')
    # writer.close()
    # await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())
