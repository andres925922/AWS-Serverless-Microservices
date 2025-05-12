import os
import logging
import logging.config
import json
import datetime
from yaml import safe_load


def config_logger():
    """
    Load the logging configuration from a YAML file.
    """
    with open(os.path.join(os.path.dirname(__file__), "config.yml"), "r") as file:
        config = safe_load(file)

    logging.config.dictConfig(config)


class JsonFormatter(logging.Formatter):
    default_time_format = '%Y-%m-%d %H:%M:%S.%fZ'

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            # 'timestamp': _setup_timestamp(record.created),
            'timestamp': self.formatTime(record, self.default_time_format),
            'logger_name': record.name,
            'severity': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'line_number': record.lineno,
            'function': record.funcName,
            'exceptionInfo': self.formatException(record.exc_info) if record.exc_info else None,
        }
        return json.dumps(log_record)