import logging
from typing import Optional

from bot.enums.base import FMSStateBaseEnum
from bot.enums.sighin_state import SighInStateEnum
from bot.modules.fms_state.base import BaseFMSState
from bot.utils.expections import UnExpectedLineException


class RegistrationFMSState(BaseFMSState):
    """
    Это Менеджер состояния процесса регистрации
    """

    def __init__(self, state: Optional[str] = None) -> None:
        """
        :param state: Состояние на момент инициализации.
        """
        try:
            t_state = SighInStateEnum(state)
        except ValueError:
            t_state = SighInStateEnum.not_sighin_user
        self._state: SighInStateEnum = t_state

    @property
    def state(self) -> FMSStateBaseEnum:
        return self._state

    def next_state(self) -> None:
        """
        Переключение состояния на следующий
        """
        if self._state == SighInStateEnum.not_sighin_user:
            self._state = SighInStateEnum.username
            return

        if self._state == SighInStateEnum.username:
            self._state = SighInStateEnum.pincode
            return

        if self.state == SighInStateEnum.pincode:
            logging.error("Pincode is last state")
            raise UnExpectedLineException()
        logging.error(f'class {self.__class__.__name__} method next_state. Unexpected line occupied for state "{self.state}"')
        raise UnExpectedLineException()
