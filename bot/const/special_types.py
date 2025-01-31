from typing import Any, Callable

from pyrogram.client import Client

from bot.const.types import HandlerFuncReturnType
from bot.utils.handler_context import HandlerContext

HandlerFuncSignatureType = Callable[[HandlerContext, Client, Any], HandlerFuncReturnType]
