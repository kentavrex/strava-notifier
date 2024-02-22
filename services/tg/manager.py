from telebot import types

from services.tg import bot, USER_CHAT_IDS


class TgManager:
    @staticmethod
    def start(chat_id: int):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton('/start')
        keyboard.add(button1)
        print(chat_id)
        USER_CHAT_IDS[chat_id] = True
        bot.send_message(chat_id, "Привет! Теперь ты будешь получать информацию о наличии свободных "
                                  "мест для записи на Strava!")

    @staticmethod
    def send_message_to_all_users(message):
        for chat_id, subscribed in USER_CHAT_IDS.items():
            if subscribed:
                bot.send_message(chat_id, message)