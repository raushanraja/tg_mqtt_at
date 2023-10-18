import asyncio
from asyncio import streams, StreamReader, StreamWriter

import logging
import sys
import traceback
import time
import os
import json
import random

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class MQTTException(Exception):
    pass

async def read_packet(reader: StreamReader):
    # Read the packet length
    # packet_length = 100
    # multiplier = 1
    while True:
        packet_type = await reader.read(1)
        print(packet_type)
        # packet_length_byte = await reader.read(1)
        # packet_length = int.from_bytes(packet_length_byte, byteorder='big')


    #     if byte == b'':
    #         raise MQTTException("Connection closed while reading packet length")
    #     packet_length += (byte[0] & 0x7F) * multiplier
    #     multiplier *= 128
    #     if byte[0] & 0x80 == 0:
    #         break
    # # Read the packet
    # packet = await reader.read(packet_length)
    # if len(packet) != packet_length:
        # raise MQTTException("Connection closed while reading packet")
    # return packet


async def write_packet(writer: StreamWriter, packet: bytes):
    # Write the packet length
    packet_length = len(packet)
    while True:
        encoded_byte = packet_length % 128
        packet_length //= 128
        if packet_length > 0:
            encoded_byte |= 0x80
        writer.write(bytes([encoded_byte]))
        if packet_length <= 0:
            break
    # Write the packet
    writer.write(packet)
    await writer.drain()


async def write_connect(writer: StreamWriter):
    # Connect packet
    packet = b'\x10\x13\x00\x04MQTT\x04\x02\x00\x3c\x00\x07client12'
    print(len(packet))
    writer.write(packet)
    await writer.drain()





async def main():
    reader, writer = await asyncio.open_connection('localhost', 1883)

    # Send CONNECT
    # await write_packet(writerk) 
    # await write_connect(writer)
    # # Receive CONNACK
    packet = await read_packet(reader)
    # print(packet)
    # # Send PUBLISH
    # await write_packet(writer, b'\x30\x0c\x00\x05topic\x00\x05hello')
    # # Receive PUBACK
    # packet = await read_packet(reader)
    # print(packet)
    # # Send DISCONNECT
    # await write_packet(writer, b'\xe0\x00')
    # writer.close()
    # await writer.wait_closed()


if __name__ == "__main__":
    asyncio.run(main())

