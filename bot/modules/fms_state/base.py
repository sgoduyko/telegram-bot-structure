from abc import ABC, abstractmethod
from typing import Optional

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
