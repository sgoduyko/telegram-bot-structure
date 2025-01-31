import io
import json
import logging
import os.path
import sys

from bot.config import (
    IS_LOG_FORMATE_AS_JSON,
    IS_WRITE_IN_CONSOLE_MODE,
    LOG_DIR_PATH,
    LOG_FILE_NAME,
)
from bot.const.const import LOG_DATE_FORMAT


class CustomJsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "time": self.formatTime(record, LOG_DATE_FORMAT),
                "level": record.levelname,
                "message": record.getMessage(),
                "file": record.filename,
                "function": record.funcName,
                "line": record.lineno,
                "process": record.process,
                "thread": record.threadName,
                "exception": self.formatException(record.exc_info) if record.exc_info else "",
            },
            ensure_ascii=False,
        )


class CustomFormatter(logging.Formatter):
    """
    Форматтер, который позваляет нам записывать дополнительные данные в лог.
    """

    def format(self, record: logging.LogRecord) -> str:
        buffer = io.StringIO()
        buffer.write(record.msg)
        if getattr(record, "telegram_user_id", None):
            buffer.write(f" - telegram_user_id=\"{getattr(record, 'telegram_user_id')}\"")
        if getattr(record, "user_id", None):
            buffer.write(f" - user_id=\"{getattr(record, 'user_id')}\"")
        if getattr(record, "fms_name", None):
            buffer.write(f" - fms_name=\"{getattr(record, 'fms_name')}\"")
        if getattr(record, "fms_data", None):
            buffer.write(f" - fms_data=\"{getattr(record, 'fms_data')}\"")
        record.msg = buffer.getvalue()
        return super().format(record)


class ConsoleInfoHandlerFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno in (logging.INFO, logging.DEBUG, logging.DEBUG)


def setup_root_logger(level: int) -> None:
    """
    Настройка логов
    :param level:
    :return:
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    if root_logger.handlers:
        # Удаляем все обработчики, которые могут быть уже добавлены.
        # Чтобы не происходило дублирования логов
        root_logger.handlers.clear()

    if IS_LOG_FORMATE_AS_JSON:
        formatter: logging.Formatter = CustomJsonFormatter()
    else:
        formatter = CustomFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt=LOG_DATE_FORMAT)

    if IS_WRITE_IN_CONSOLE_MODE:
        # Обработчик для вывода debug, info, warning
        info_console_handler = logging.StreamHandler(sys.stdout)
        info_console_handler.setLevel(level)
        info_console_handler.setFormatter(formatter)
        info_console_handler.addFilter(ConsoleInfoHandlerFilter())  # Не выводим логи выше warning
        root_logger.addHandler(info_console_handler)

        # Обработчик для вывода error, critical
        err_console_handler = logging.StreamHandler(sys.stderr)
        err_console_handler.setLevel(logging.ERROR)
        err_console_handler.setFormatter(formatter)
        root_logger.addHandler(err_console_handler)

    # Обработчик для записи в файл
    # todo есть вопрос по записи логов в файл.
    #  Так как код асинхронный, то запись происходит либо при завершении работы, либо через некоторое время
    #  бота. Для записи в реальном времени нужно переходить на aiologger
    file_handler = logging.FileHandler(str(os.path.join(LOG_DIR_PATH, LOG_FILE_NAME)), mode="a", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
