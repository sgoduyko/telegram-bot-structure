from typing import Optional, Tuple

from bot.config import REDIS_OPERATION_DELIMITER
from bot.const.types import TFMSData, TFMSName
from redis_db.client import redis_default


async def get_fms_data(user_id: int) -> Tuple[Optional[TFMSName], Optional[TFMSData]]:
    """
    Здесь у получение fms данных по User.id
    Это основной способ хранения fms процессов в системе.
    Только вход и регистрация хранятся по telegram_user_id
    :param user_id: User.id пользователя системы
    :return: fms_name и fms_data
    """

    user_data: Optional[str] = await redis_default.get(str(user_id))
    if not user_data:
        return None, None

    fms_name, fms_data = user_data.split(REDIS_OPERATION_DELIMITER)
    if fms_name is not None:
        fms_name = TFMSName(fms_name)

    if fms_data is not None:
        fms_data = TFMSData(fms_data)
    return fms_name, fms_data
