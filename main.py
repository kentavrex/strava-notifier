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

AUTH_TOKEN = ''


def get_special_projects():
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    resp = requests.get("https://my.itmo.ru/api/sport/my_sport/spec_projects", headers=headers)
    try:
        return resp.json()["result"]
    except Exception as e:
        logging.error(f"Internal error:={e}")


def refresh_access_token_without_secret(refresh_token, client_id, token_url, realm):
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
    }

    response = requests.post(f'{token_url}/realms/{realm}/protocol/openid-connect/token', data=data)

    if response.status_code == 200:
        new_access_token = response.json().get('access_token')
        return new_access_token
    else:
        print(f"Ошибка при обновлении access token: {response.status_code}, {response.text}")
        return None


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
            logging.info("Trying to get refreshed access token")
            AUTH_TOKEN = refresh_access_token_without_secret(refresh_token=config.KEYCLOACK_REFRESH_TOKEN,
                                                             client_id=config.KEYCLOACK_CLIENT_ID,
                                                             token_url='https://id.itmo.ru/auth',
                                                             realm='itmo')
        else:
            time.sleep(10)
