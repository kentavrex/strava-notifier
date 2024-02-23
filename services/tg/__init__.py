import telebot
from telebot import types

from config import config

USER_CHAT_IDS = {633824907}

bot = telebot.TeleBot(config.TG_TOKEN)

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(types.KeyboardButton('/start'))
keyboard.add(types.KeyboardButton('/ping'))
keyboard.add(types.KeyboardButton('/stop'))
