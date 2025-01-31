import asyncio
import logging
import sys
from typing import Callable, Optional

from pyrogram.filters import Filter

from bot.const.const import HANDLERS_LIST_VAR_NAME
from bot.const.dataclasses import HandlerObj
from bot.const.special_types import HandlerFuncSignatureType
from bot.const.types import THandlerUploadOrderNumber
from bot.utils.get_caller_module import get_caller_module


# P = ParamSpec("P")


# HandlerFuncSignatureType = Callable[[HandlerContext, Client, THandler], HandlerFuncReturnType]

# HHHH = Callable[[HandlerContext, Client, THandler], Coroutine[Any, Any, HandlerFuncReturnType]]


# @overload
# def add_handler_with_filters(order: THandlerUploadOrderNumber, filters: Optional[Filter]) -> Callable[[Callable[[HandlerContext, Client, Message], HandlerFuncReturnType]], None]: ...
#
#
# @overload
# def add_handler_with_filters(order: THandlerUploadOrderNumber, filters: Optional[Filter]) -> Callable[[Callable[[HandlerContext, Client, CallbackQuery], HandlerFuncReturnType]], None]: ...


def add_handler_with_filters(order: THandlerUploadOrderNumber, filters: Optional[Filter]) -> Callable[[HandlerFuncSignatureType], None]:
    """
    Декоратор, который добавляет функцию-обработчик.
    """

    def wrapper(func: HandlerFuncSignatureType) -> None:
        if not asyncio.iscoroutinefunction(func):
            logging.error("We don't support synchronous handlers")
            raise Exception("We don't support synchronous handlers")
        module_name: Optional[str] = get_caller_module()
        if module_name is None:
            logging.error("Module name where is calling handler func not found")
            raise Exception("Module name where is calling handler func not found")
        current_module = sys.modules[module_name]
        current_module.__dict__[HANDLERS_LIST_VAR_NAME].append(
            HandlerObj(
                handler_name=func.__name__,
                func=func,
                register_number=order,
                filters=filters,
            )
        )

    return wrapper
