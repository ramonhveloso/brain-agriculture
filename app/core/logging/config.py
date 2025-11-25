import logging
import logging.config
import os

import structlog

from .processors import add_timestamp, remove_exc_info, rename_event_key

LOG_FILE_PATH = "logs/app.log"

os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)


def setup_logging():
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {"format": "%(message)s"},
                "structured_json": {
                    "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "fmt": "%(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "plain",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": LOG_FILE_PATH,
                    "maxBytes": 5 * 1024 * 1024,
                    "backupCount": 5,
                    "encoding": "utf8",
                    "formatter": "structured_json",
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": "INFO",
            },
        }
    )

    structlog.configure(
        processors=[
            add_timestamp,
            structlog.processors.add_log_level,
            rename_event_key,
            remove_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )
