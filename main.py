import os
import threading
import time

import logging.config
import services.tg.api  # noqa
from config import config
from services.my_itmo import MyITMOService
from services.tg import bot
from services.tg.manager import TgManager


def init_logger():
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_config.conf')
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
    logging.getLogger().setLevel(level=os.environ.get("RACKS_LOG_LEVEL", "INFO"))


init_logger()

SLEEP_TIME = 10 * 60


def send_notifications(message_info: str | None, repeat_count: int = 100) -> None:
    if not message_info:
        return

    for _ in range(repeat_count):
        TgManager.send_message_to_all_users(message_info)
        time.sleep(10)


def main(my_itmo_service: MyITMOService):
    try:
        message_info = my_itmo_service.find_free_places()
    except ConnectionError as err:
        logging.error(err)
        try:
            logging.info("Trying to get refreshed access token")
            my_itmo_service.refresh_access_token_without_secret(refresh_token=config.KEYCLOACK_REFRESH_TOKEN,
                                                                client_id=config.KEYCLOACK_CLIENT_ID,
                                                                token_url=config.KEYCLOACK_TOKEN_URL,
                                                                realm=config.KEYCLOACK_REALM)
        except ConnectionError as err:
            logging.error(err)
            send_notifications(message_info="Update refresh token", repeat_count=5)
            raise ConnectionError(err)
    else:
        send_notifications(message_info=message_info)
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    threading.Thread(target=lambda: bot.polling(none_stop=True)).start()
    my_itmo_service = MyITMOService()
    try:
        while True:
            main(my_itmo_service=my_itmo_service)
    except Exception as err:
        logging.error(err)
