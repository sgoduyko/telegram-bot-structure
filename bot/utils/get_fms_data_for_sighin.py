from typing import Optional, Tuple

from bot.config import REDIS_OPERATION_DELIMITER
from bot.const.types import TFMSData, TFMSName, TTelegramUserId
from redis_db.client import redis_login


async def get_fms_data_for_registration(telegram_user_id: TTelegramUserId) -> Tuple[Optional[TFMSName], Optional[TFMSData]]:
    """
    Получаем данные для fms по telegram_user_id.
    Такой формат используется только для регистрации и входа пользователя в систему
    :param telegram_user_id:
    :return: fms_name, fms_data
    """
    user_data: Optional[str] = await redis_login.get(str(telegram_user_id))
    if user_data:
        fms_name, fms_data = user_data.split(REDIS_OPERATION_DELIMITER)
    else:
        fms_name, fms_data = None, None

    if fms_name is not None:
        fms_name = TFMSName(fms_name)

    if fms_data is not None:
        fms_data = TFMSData(fms_data)
    return fms_name, fms_data
