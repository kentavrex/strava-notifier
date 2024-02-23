import logging

from services.tg import bot, USER_CHAT_IDS, keyboard


class TgManager:
    @staticmethod
    def start(chat_id: int):
        USER_CHAT_IDS.add(chat_id)
        logging.info(f"chat_id={chat_id} added")
        bot.send_message(chat_id, "Привет! Теперь ты будешь получать информацию о наличии свободных "
                                  "мест для записи на Strava!", reply_markup=keyboard)

    @staticmethod
    def ping(chat_id: int):
        logging.info(f"ping from chat_id={chat_id}")
        bot.send_message(chat_id, "Ok", reply_markup=keyboard)

    @staticmethod
    def stop(chat_id: int):
        USER_CHAT_IDS.remove(chat_id)
        logging.info(f"chat_id={chat_id} removed")
        bot.send_message(chat_id, "Уведомления приостановлены!", reply_markup=keyboard)

    @staticmethod
    def send_message_to_all_users(message) -> None:
        for chat_id in USER_CHAT_IDS:
            try:
                bot.send_message(chat_id, message)
            except Exception as err:
                raise ConnectionError(f"Tg bot request error={err}")
