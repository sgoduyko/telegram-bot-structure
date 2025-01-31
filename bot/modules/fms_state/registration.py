import logging
from typing import Optional

from bot.const.const import PINCODE_REQUIREMENTS_TEXT, USERNAME_REQUIREMENTS_TEXT
from bot.const.types import TReplyToUserText
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
        super().__init__(state)
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

    def is_not_sighin_user_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.not_sighin_user.value)

    def is_username_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.username.value)

    def is_pincode_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.pincode.value)

    def get_reply_text_for_current_state(self) -> TReplyToUserText:
        """Получить текст сообщения пользователю, для текущего состояния"""
        if self.is_not_sighin_user_state():
            logging.error("Unexpected user state")
            raise UnExpectedLineException("Unexpected user state")
        if self.is_username_state():
            return TReplyToUserText(f"Введите логин. {USERNAME_REQUIREMENTS_TEXT}")
        if self.is_pincode_state():
            return TReplyToUserText(f"Введите пинкод. {PINCODE_REQUIREMENTS_TEXT}")

        logging.error("Unexpected line")
        raise UnExpectedLineException("Unexpected user state")
