import logging
from datetime import datetime
import json

from chalicelib.configs import config


class FormatterJSON(logging.Formatter):
    def format(self, record: logging.LogRecord):
        j = {
            'level': record.levelname,
            'timestamp': datetime.now().timestamp(),
            'name': record.module,
            'message': record.getMessage(),
            'aws_request_id': getattr(record, 'aws_request_id', '00000000-0000-0000-0000-000000000000'),
            'context': record.__dict__.get('data', {})
        }
        return json.dumps(j)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    log_level = logging.getLevelName(config.LOG_LEVEL)
    logger.setLevel(log_level)

    formatter = FormatterJSON(
        '[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(levelno)s\t%(message)s\n',
        '%Y-%m-%dT%H:%M:%S'
    )
    logger.handlers[0].setFormatter(formatter)

    return logger
