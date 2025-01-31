import logging
from typing import List, Optional, Tuple

from bot.config import (
    PINCODE_PATTERN,
    REDIS_FMS_DATA_DELIMITER,
    REDIS_OPERATION_DELIMITER,
    USERNAME_PATTERN,
)
from bot.const.const import (
    PINCODE_REQUIREMENTS_TEXT,
    REGISTRATION_FMS_NAME,
    REGISTRATION_UNEXPECTED_LINE_ERR_TEXT,
    USERNAME_REQUIREMENTS_TEXT,
)
from bot.const.types import TReplyToUserText
from bot.enums.sighin_state import SighInStateEnum
from bot.modules.fms_data_pipeline.base import BaseFMSDataPipeline
from bot.modules.fms_state.base import BaseFMSState
from bot.modules.fms_state.registration import RegistrationFMSState
from bot.utils.expections import UnExpectedLineException
from bot.utils.handler_context import HandlerContext
from db.functions.user.create_user import create_user
from db.functions.user.soft_get_user_by_username import soft_get_user_by_id
from db.functions.user.update_user import update_user_pincode
from redis_db.client import redis_login, redis_session


class SighInFMSDataPipeline(BaseFMSDataPipeline):
    """
    Процесс регистрации пользователя
    """

    def __init__(self, ctx: HandlerContext, fms_data: Optional[str]) -> None:
        state: Optional[str] = None
        user_id: Optional[str] = None
        if fms_data is not None:
            state, user_id = fms_data.split(REDIS_FMS_DATA_DELIMITER)

        self._user_reply_list: List[TReplyToUserText] = []
        self.__fms: BaseFMSState = RegistrationFMSState(state)
        self.__ctx: HandlerContext = ctx
        self.__ctx.expend_logging_extra({"fms_state": self.state.name})

        self._fms_name: str = REGISTRATION_FMS_NAME

        if user_id:
            self.user_id: Optional[int] = int(user_id)
        else:
            self.user_id = None

    @property
    def _fms(self) -> BaseFMSState:
        return self.__fms

    @property
    def _ctx(self) -> HandlerContext:
        return self.__ctx
    async def init_data(self) -> None:
        """
        Если нужно инициализировать какие-то данные, то это делается здесь
        """
        self._is_data_inited = True
        user = None
        if self.user_id is not None:
            user = await soft_get_user_by_id(self._ctx, self.user_id)

        if user:
            self._ctx.update_user(user)

        if self.is_pincode_state() and not user:
            logging.warning("User not found", extra=self._ctx.get_logging_extra())
            raise Exception("Pincode stage, but user not found")

    def get_key_and_value_data(self) -> Tuple[int, str]:
        return self._ctx.telegram_user_id, (
            f"{self._fms_name}{REDIS_OPERATION_DELIMITER}{self.state.value}" f"{REDIS_FMS_DATA_DELIMITER}{self.user_id or ''}"
        )

    def is_not_sighin_user_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.not_sighin_user.value)

    def is_username_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.username.value)

    def is_pincode_state(self) -> bool:
        return bool(self.state.value == SighInStateEnum.pincode.value)

    def validate_data(self) -> None:
        if not getattr(self, "_is_data_inited", False):
            logging.warning("Data is not initialized", extra=self._ctx.get_logging_extra())
            raise Exception("Data is not initialized")

        logging.debug("Validation process started.", extra=self._ctx.get_logging_extra())
        self._is_validated = True
        self._is_data_valid = True

        if self.is_not_sighin_user_state():
            return

        if self.is_username_state():
            if not USERNAME_PATTERN.fullmatch(self._ctx.message.text):
                self.add_user_reply(f"Никнейм не соответствует требованиям. {USERNAME_REQUIREMENTS_TEXT}")
                logging.debug("Username is incorrect", extra=self._ctx.get_logging_extra())
                self._is_data_valid = False
            return

        if self.is_pincode_state():
            if not PINCODE_PATTERN.fullmatch(self._ctx.message.text):
                self.add_user_reply(f"Пинкод не соответствует требованиям. {PINCODE_REQUIREMENTS_TEXT}")
                logging.debug("Pincode is incorrect", extra=self._ctx.get_logging_extra())
                self._is_data_valid = False
                return
            if not self._ctx.user:
                logging.error("User didn't set", extra=self._ctx.get_logging_extra())
                self._is_data_valid = False
                raise Exception(f"Registration. Pincode state. User not found")
            return

        logging.debug("Validation data. Unexpected point", extra=self._ctx.get_logging_extra())

    async def process_pipeline(self) -> None:
        logging.debug("Processing pipeline data", extra=self._ctx.get_logging_extra())

        if not getattr(self, "_is_validated", False):
            logging.warning("Pipeline's data didn't validate yet", extra=self._ctx.get_logging_extra())
            raise Exception("Pipeline's data didn't validate yet.")

        if self.is_not_sighin_user_state():
            self._fms.next_state()
            key, value = self.get_key_and_value_data()
            await redis_login.set(str(key), value)
            self.add_user_reply("Введите логин")
            return

        if self.is_username_state():
            logging.debug("Creating user", extra=self._ctx.get_logging_extra())
            user = await create_user(self._ctx, self._ctx.message.text)

            if not user:
                logging.debug("Username is duplicate", extra=self._ctx.get_logging_extra())
                self.add_user_reply("Никнейм уже занят. Нужно подобрать что-то другое.")
                return
            logging.debug("User created", extra=self._ctx.get_logging_extra())
            self._fms.next_state()
            self._ctx.update_user(user)
            self.user_id = int(user.id) if user else None
            key, value = self.get_key_and_value_data()
            logging.debug("Save telegram user id and stage fms in redis", extra=self._ctx.get_logging_extra())
            await redis_login.set(str(key), value)
            logging.debug("Data saved in redis", extra=self._ctx.get_logging_extra())
            self.add_user_reply(f"Введите пинкод. {PINCODE_REQUIREMENTS_TEXT}")
            return

        if self.is_pincode_state():
            logging.debug("Update pincode", extra=self._ctx.get_logging_extra())
            await update_user_pincode(self._ctx, self._ctx.user, int(self._ctx.message.text))
            logging.debug("deleting fms data from redis", extra=self._ctx.get_logging_extra())
            await redis_login.delete(str(self._ctx.telegram_user_id))
            logging.debug("Create user session in redis", extra=self._ctx.get_logging_extra())
            user_id = self._ctx.user.id if self._ctx.user else None
            if user_id is not None:
                await redis_session.set(str(self._ctx.telegram_user_id), int(user_id))
                logging.info(f"Новая сессия добавления для пары telegram_user_id: {self._ctx.telegram_user_id}; user_id: {user_id}")
            self.add_user_reply(f"Пользователь успешно создан. " f"Вы можете начать работать с нашим интерфейсом задач /tasks")
            return
        raise UnExpectedLineException(REGISTRATION_UNEXPECTED_LINE_ERR_TEXT)
