import json
import logging
from datetime import datetime


class JsonFormatter(logging.Formatter):
    """
    Класс необходим для решения проблемы экранирования двойных кавычек в логе
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def formatMessage(self, record: logging.LogRecord) -> str:
        super().formatMessage(record)

        log_record = {
            "timestamp": datetime.utcfromtimestamp(record.created).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "level": record.levelname,
            "file": record.filename,
            "message": record.message
        }

        return json.dumps(log_record)
