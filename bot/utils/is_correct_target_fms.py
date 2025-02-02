from typing import Optional

from bot.const.types import TFMSName


def is_correct_target_fms(target_fm: TFMSName, active_fms: Optional[TFMSName]) -> bool:
    """
    Проверяет, отличается ли fms обработчика и fms, который у пользователя в процессе.
    :param target_fm: fms обработчика
    :param active_fms: fms, который у пользователя в процессе
    :return:
    """
    if not active_fms:
        return True
    if target_fm == active_fms:
        return True

    return False
