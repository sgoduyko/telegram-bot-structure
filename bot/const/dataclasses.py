import dataclasses
from typing import Any, Callable, Coroutine, Optional

from pyrogram.filters import Filter

from bot.const.types import THandlerUploadOrderNumber


@dataclasses.dataclass
class HandlerObj:
    """
    Объект, в который мы кладем все данные по обработчику, во время сбора всех обработчиков.
    """

    handler_name: str
    func: Callable[..., Coroutine[Any, Any, None]]
    register_number: THandlerUploadOrderNumber
    filters: Optional[Filter]
