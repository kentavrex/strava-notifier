from services.tg import bot
from services.tg.manager import TgManager


@bot.message_handler(commands=['start'])
def handle_start(message):
    return TgManager.start(chat_id=message.chat.id)


@bot.message_handler(commands=['ping'])
def handle_ping(message):
    return TgManager.ping(chat_id=message.chat.id)


@bot.message_handler(commands=['stop'])
def handle_stop(message):
    return TgManager.stop(chat_id=message.chat.id)
