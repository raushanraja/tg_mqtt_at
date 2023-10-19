import os
import dotenv
from telebot.async_telebot import AsyncTeleBot, State, types
from telebot.asyncio_handler_backends import StatesGroup
import logging

from tgreply import ReplyManager, ReplyManageType, ReplyData
from q import shared_queue, Message, Direction, MessageType

dotenv.load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bot = AsyncTeleBot(TOKEN)
reply_manager = ReplyManager(bot)


@bot.message_handler(commands=['sms'])
async def send_sms(message):
    markup = types.ForceReply(selective=False)
    sent_message  = await bot.send_message(message.chat.id, "Enter the number to send SMS", reply_markup=markup)
    reply_manager.add(ReplyData(message.chat.id, sent_message.id, ReplyManageType.SMSNUMBER))


@bot.message_handler(commands=['location'])
async def get_location(message):
    msg = message.text.split(' ')[1:]
    if len(msg) > 0:
        await shared_queue.put(Message(message=msg[0], direction=Direction.MQTT, message_type=MessageType.LOCATION))
    else:
        await shared_queue.put(Message(message='get', direction=Direction.MQTT, message_type=MessageType.LOCATION))


@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    # await bot.reply_to(message, message.text)
    if message.reply_to_message:
        chat_id = message.chat.id
        message_id = message.reply_to_message.message_id
        await reply_manager.handle_reply(chat_id, message_id, message)
    else:
        await shared_queue.put(Message(message=message.text, direction=Direction.MQTT))
