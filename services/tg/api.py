from services.tg import bot
from services.tg.manager import TgManager


@bot.message_handler(commands=['start'])
def handle_start(message):
    return TgManager.start(chat_id=message.chat.id)

