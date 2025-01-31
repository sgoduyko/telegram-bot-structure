from abc import ABC, abstractmethod
from typing import Optional

from bot.const.types import TReplyToUserText
from bot.enums.base import FMSStateBaseEnum


class BaseFMSState(ABC):
    def __init__(self, state: Optional[str] = None) -> None:
        """
        :param state: Состояние на момент инициализации.
        """

    @property
    @abstractmethod
    def state(self) -> FMSStateBaseEnum:
        pass

    @abstractmethod
    def next_state(self) -> None:
        """
        Переключение состояния на следующее
        """

    @abstractmethod
    def get_reply_text_for_current_state(self) -> TReplyToUserText:
        """
        Возвращает текст сообщения, в зависимости о состояния
        :return: текст сообщения пользователю
        """
