from typing import Dict, Optional, Union

from pyrogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.const.types import TFMSData, TFMSName, TTelegramUserId
from db.models.user import User


class HandlerContext:
    """
    Контекст обработчика.
    В нем мы собираем всю предварительную информацию, которая понадобится в обработчике
    """

    def __init__(
        self,
        session: AsyncSession,
        telegram_user_id: TTelegramUserId,
        user: Optional[User],
        fms_name: Optional[TFMSName],
        fms_data: Optional[TFMSData],
        message: Message,
    ) -> None:
        self.session: AsyncSession = session
        self.telegram_user_id: TTelegramUserId = telegram_user_id
        self.user: Optional[User] = user
        logging_extra: Dict[str, Union[str, int]] = {"telegram_user_id": int(telegram_user_id)}
        # logging_extra = {"telegram_user_id": 123, "user_id": 1, "fms_name": "registration"}

        if user:
            logging_extra.update({"user_id": int(user.id)})
        if fms_name:
            logging_extra.update({"fms_name": fms_name})
        if fms_data:
            logging_extra.update({"fms_data": fms_data})

        self._logging_extra: Dict[str, Union[str, int]] = logging_extra
        self.fms_name: Optional[TFMSName] = fms_name
        self.fms_data: Optional[TFMSData] = fms_data

        self._message: Message = message

    def expend_logging_extra(self, extra: Dict[str, Union[str, int]]) -> None:
        self._logging_extra.update(extra)

    def update_user(self, user: User) -> None:
        self.user = user
        self._logging_extra.update({"user_id": int(user.id)})

    def get_logging_extra(self) -> Dict[str, Union[str, int]]:
        return self._logging_extra

    def update_fms_name(self, fms_name: TFMSName) -> None:
        self.fms_name = fms_name
        self._logging_extra.update({"fms_name": fms_name})

    @property
    def is_fms_pipeline(self) -> bool:
        return bool(self.fms_name is not None)

    @property
    def message(self) -> Message:
        return self._message
