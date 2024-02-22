import logging.config
import os
import threading
import time
import services.tg.api  # noqa

import requests

from config import config
from services.tg import bot
from services.tg.manager import TgManager


def init_logger():
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_config.conf')
    logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
    logging.getLogger().setLevel(level=os.environ.get("RACKS_LOG_LEVEL", "INFO"))


init_logger()


def get_special_projects():
    headers = {
        "Authorization": config.AUTH_TOKEN
    }
    resp = requests.get("https://my.itmo.ru/api/sport/my_sport/spec_projects", headers=headers)
    try:
        return resp.json()["result"]
    except Exception as e:
        logging.error(f"Internal error:={e}")


def main():
    available, limit = None, None
    for special_course in get_special_projects():
        if special_course["name"] != 'Kronbars Running':
            continue
        available = special_course["available"]
        limit = special_course["limit"]

    if None not in [limit, available]:
        # TgManager.send_message_to_all_users(f"Available: {available}/{limit} places")
        logging.info(f"Available: {available}/{limit} places")
        if available > 0:
            for _ in range(100):
                TgManager.send_message_to_all_users(f"Available: {available}/{limit} places")
                time.sleep(5)
    else:
        logging.info("Internal error")
        raise Exception()


if __name__ == "__main__":
    threading.Thread(target=lambda: bot.polling(none_stop=True)).start()
    while True:
        try:
            main()
        except Exception:
            TgManager.send_message_to_all_users(f"No free places found. Restart the script with new Bearer token!")
            logging.error("Error")
            # TODO if error -> Need re-login and get new Authorization Bearer token
            exit(1)
        else:
            time.sleep(60)

