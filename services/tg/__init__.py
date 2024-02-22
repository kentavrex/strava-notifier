import telebot

from config import config

USER_CHAT_IDS = {633824907: True}

bot = telebot.TeleBot(config.TG_TOKEN)
