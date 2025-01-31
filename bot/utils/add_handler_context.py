import logging
from typing import Any, Callable, Coroutine, Optional, ParamSpec

from pyrogram.client import Client
from pyrogram.types import CallbackQuery, Message
from pyrogram.types.object import Object
from pyrogram.types.update import Update
from sqlalchemy.exc import PendingRollbackError
from sqlalchemy.future import select

from bot.const.const import INTERNAL_ERROR_TEXT
from bot.const.types import TFMSData, TFMSName, TTelegramUserId
from bot.utils.add_handler_with_filters import HandlerFuncSignatureType
from bot.utils.get_fms_data import get_fms_data
from bot.utils.get_fms_data_for_sighin import get_fms_data_for_registration
from bot.utils.handler_context import HandlerContext
from db.models.user import User
from db.session_factory import AsyncSessionLocal
from redis_db.client import redis_session


class CommonType(Object, Update):
    pass


# THandler = TypeVar('THandler', bound=Union[CallbackQuery, Message])
P = ParamSpec("P")
HandlerFuncReturnType = Coroutine[Any, Any, None]  # функция либо асинхронная, либо синхронная. Возможны оба варианта
# HandlerFuncSignatureType = Callable[[HandlerContext, Client, THandler], HandlerFuncReturnType]


# @overload
# def add_handler_context(
#     func: Callable[[HandlerContext, Client, Message], HandlerFuncReturnType],
# ) -> Callable[[Client, Message], HandlerFuncReturnType]:
#     async def wrapper(client: Client, obj: Message) -> None: ...
#
#     return wrapper
#
#
# @overload
# def add_handler_context(
#     func: Callable[[HandlerContext, Client, CallbackQuery], HandlerFuncReturnType],
# ) -> Callable[[Client, CallbackQuery], HandlerFuncReturnType]:
#     async def wrapper(client: Client, obj: CallbackQuery) -> None: ...
#
#     return wrapper


def add_handler_context(
    func: HandlerFuncSignatureType,
) -> Callable[[Client, Any], HandlerFuncReturnType]:
    async def wrapper(client: Client, obj: Any) -> None:
        if not isinstance(obj, Message) and not isinstance(obj, CallbackQuery):
            logging.error(f"we met unknown obj {obj.__class__.__name__}")
            raise Exception(f"unknown obj {obj.__class__.__name__}")
        telegram_user_id: TTelegramUserId = TTelegramUserId(obj.from_user.id)

        async with AsyncSessionLocal() as session:
            user_id = await redis_session.get(str(obj.from_user.id))
            user: Optional[User] = None
            if user_id:
                query_result = await session.execute(select(User).filter(User.id == int(user_id)))
                user = query_result.scalar_one_or_none()

            fms_name: Optional[TFMSName] = None
            fms_data: Optional[TFMSData] = None

            if user:
                fms_name, fms_data = await get_fms_data(int(user.id))

            if not user:
                fms_name, fms_data = await get_fms_data_for_registration(telegram_user_id)

            msg = obj if isinstance(obj, Message) else obj.message
            ctx = HandlerContext(
                session=session, telegram_user_id=telegram_user_id, user=user, fms_name=fms_name, fms_data=fms_data, message=msg
            )
            await func(ctx, client, obj)

            try:
                await session.commit()
                # strange, because i use await
            except PendingRollbackError:
                await session.rollback()
            except Exception as err:
                logging.error(err, extra=ctx.get_logging_extra())
                await ctx.message.reply(INTERNAL_ERROR_TEXT)
            finally:
                await session.close()

    return wrapper
