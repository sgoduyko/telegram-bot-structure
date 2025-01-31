import logging
from abc import ABC, abstractmethod
from typing import Any, List, Tuple

from bot.config import CHECK_FMS_PIPELINE_CALLING_ORDER
from bot.const.types import TMethodName, TReplyToUserText
from bot.enums.base import FMSStateBaseEnum
from bot.modules.fms_state.base import BaseFMSState
from bot.utils.handler_context import HandlerContext


class LoggingMethodCallingOrderMixin:

    def __getattribute__(self, name: str) -> Any:
        """
        Здесь мы проверяем корректность вызова методов, чтобы исключить потери какого-то из этапов.
        """
        if not CHECK_FMS_PIPELINE_CALLING_ORDER:
            return super().__getattribute__(name)

        logging.debug(f"Call of method {name}")
        attr = super().__getattribute__(name)
        if name not in ("init_data", "validate_data", "process_pipeline", "mark_data_as_valid", "is_data_valid"):
            logging.debug(f"Method {name} not in list for check")
            return attr

        if name == "init_data":
            self.call_method_list.append(TMethodName(name))
            return attr

        if name == "validate_data":
            self.call_method_list.append(TMethodName(name))
            if "init_data" not in self.call_method_list:
                logging.error(f"method {name} didn't call before method init_data")
                raise Exception(f"method {name} didn't call before method init_data")

        if name == "process_pipeline":
            self.call_method_list.append(TMethodName(name))
            if "validate_data" not in self.call_method_list:
                logging.error(f"method {name} didn't call before method validate_data")
                raise Exception(f"method {name} didn't call before method validate_data")

        if name == "is_data_valid":
            self.call_method_list.append(TMethodName(name))
            if "validate_data" not in self.call_method_list:
                logging.error(f"method {name} didn't call before method mark_data_as_valid")
                raise Exception(f"method {name} didn't call before method mark_data_as_valid")

        logging.debug(f"Method {name} completed work.")
        return attr


class BaseFMSDataPipeline(ABC):
    """
    Класс-шаблон написания реализации FMS (Finite Machine State)
    """

    def __init__(self, ctx: HandlerContext) -> None:
        self._user_reply_list: List[TReplyToUserText] = []
        self.call_method_list: List[TMethodName] = []

    @property
    @abstractmethod
    def fms(self) -> BaseFMSState:
        pass

    @property
    @abstractmethod
    def _ctx(self) -> HandlerContext:
        pass

    @abstractmethod
    async def process_pipeline(self) -> None:
        """
        Основной метод обработки данных в процессе.
        Здесь мы реализуем все состояния процесса и действия по каждому состоянию.
        """

    @abstractmethod
    def get_key_and_value_data(self) -> Tuple[int, str]:
        """Возвращаем данные, которые будем класть в redis"""

    @abstractmethod
    def validate_data(self) -> None:
        """
        Проверка данных на корректность
        """

    def next_state(self) -> None:
        """
        Перенести статус процесс на следующий уровень
        :return:
        """
        self.fms.next_state()

    @property
    def state(self) -> FMSStateBaseEnum:
        """
        Текущий статус процесса
        """
        return self.fms.state

    async def init_data(self) -> None:
        """
        Для случая, когда нужно какие-то данные запросить в базе, до начала проверки данных.
        """

    def get_user_reply_list(self) -> List[TReplyToUserText]:
        """
        Получить список всех сообщений, которые мы отправим пользователю
        """
        return self._user_reply_list

    def add_user_reply(self, text: str) -> None:
        """
        Добавить сообщение в список на отправку ответа пользователю
        :param text: текст сообщения
        """
        self._user_reply_list.append(TReplyToUserText(text))

    def mark_data_as_valid(self) -> None:
        """
        Пометить данные как правильные
        """
        self._is_data_valid = True

    def is_data_valid(self) -> bool:
        """
        Вернуть информацию статуса проверки данных
        """
        return bool(getattr(self, "_is_data_valid", False))
