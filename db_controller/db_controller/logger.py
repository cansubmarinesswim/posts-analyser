import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(
        self, name: str, console_log_level: str, file_log_level: str, file_log_dir: str
    ):

        Path(file_log_dir).mkdir(parents=True, exist_ok=True)

        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        self._formatter = logging.Formatter(
            "[%(asctime)s - %(levelname)s] %(funcName)s() - %(message)s"
        )

        self._stream_handler = logging.StreamHandler(stream=sys.stdout)
        self._stream_handler.setLevel(console_log_level)
        self._stream_handler.setFormatter(self._formatter)

        self._file_handler = TimedRotatingFileHandler(
            filename=(file_log_dir + "/posts_analyser_service_database_connector_log.txt"),
            when="midnight",
        )
        self._file_handler.setLevel(file_log_level)
        self._file_handler.setFormatter(self._formatter)

        self._logger.addHandler(self._stream_handler)
        self._logger.addHandler(self._file_handler)

    @property
    def logger(self):
        return self._logger
