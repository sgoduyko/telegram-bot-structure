from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from bot.const.types import TReplyToUserText
from bot.enums.base import FMSStateBaseEnum
from bot.modules.fms_state.base import BaseFMSState
from bot.utils.handler_context import HandlerContext


class BaseFMSDataPipeline(ABC):
    """
    Класс-шаблон написания реализации FMS (Finite Machine State)
    """

    def __init__(self, ctx: HandlerContext, fms_data: Optional[str]) -> None:
        self._user_reply_list: List[TReplyToUserText] = []
        # self._fms: Type[BaseFMSState] = BaseFMSState()

    @property
    @abstractmethod
    def _fms(self) -> BaseFMSState:
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
        self._fms.next_state()

    @property
    def state(self) -> FMSStateBaseEnum:
        """
        Текущий статус процесса
        """
        return self._fms.state

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

    # def __call__(self, *args, **kwargs) -> None:
    #     """
    #     Здесь мы проверяем корректность вызова методов, чтобы исключить потери какого-то из этапов.
    #     """
    #     if not CHECK_FMS_PIPELINE_CALLING_ORDER:
    #         return
    #     function_name = inspect.stack()[1].function
    #
    #     logging.debug(f"Class {self.__class__.__name__}. Call of method {function_name}", extra=self._ctx.get_logging_extra())
    #
    #     if function_name == "init_data":
    #         await self.init_data()
    #         self.is_init_data_called = True
    #
    #     if function_name == "validate_data":
    #         if not getattr(self, "is_init_data_called", False):
    #             logging.error(f"method {function_name} didn't call before method init_data", extra=self._ctx.get_logging_extra())
    #             raise Exception(f"method {function_name} didn't call before method init_data")
    #
    #         self._validate_data_in_progress = True
    #         self.validate_data()
    #         del self._validate_data_in_progress
    #         self.is_validate_data_called = True
    #
    #     if function_name == "process_pipeline":
    #         if not getattr(self, "is_validate_data_called", False):
    #             logging.error(f"method {function_name} didn't call before method validate_data", extra=self._ctx.get_logging_extra())
    #             raise Exception(f"method {function_name} didn't call before method validate_data")
    #
    #     # Методы работы со статусов проверки данных
    #     if function_name == "mark_data_as_valid":
    #         if not getattr(self, "_validate_data_in_progress", False):
    #             logging.error(f"method {function_name} didn't call before method validate_data", extra=self._ctx.get_logging_extra())
    #             raise Exception(f"method {function_name} didn't call before method validate_data")
    #         self.mark_data_as_valid()
    #         self.is_mark_data_valid_called = True
    #
    #     if function_name == "is_data_valid":
    #         if not getattr(self, "is_mark_data_valid_called", False):
    #             logging.error(f"method {function_name} didn't call before method mark_data_as_valid", extra=self._ctx.get_logging_extra())
    #             raise Exception(f"method {function_name} didn't call before method mark_data_as_valid")
    #
    #     logging.debug(f"Class {self.__class__.__name__}. Method {function_name} completed work.", extra=self._ctx.get_logging_extra())
