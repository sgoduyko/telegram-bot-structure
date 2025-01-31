from pyrogram.client import Client
from pyrogram.types import Message

from bot.const import handlers_order
from bot.modules.fms_data_pipeline import fms_pool
from bot.utils.add_handler_with_filters import add_handler_with_filters
from bot.utils.handler_context import HandlerContext
from bot.utils.reply_to_user import reply_to_user


@add_handler_with_filters(order=handlers_order.MESSAGE_HANDLE_ALL_MESSAGE__ORDER_NUMBER, filters=None)
async def message_handle_all_message(ctx: HandlerContext, client: Client, message: Message) -> None:
    """
    Мы обрабатываем все сообщения, которые пишет нам пользователь.
    Мы смотрим, есть ли у пользователя активная сессия или какая-то операция в процессе
    """
    fms_pipeline = fms_pool.get_pipeline(ctx.fms_name)(ctx)

    await fms_pipeline.init_data()
    fms_pipeline.validate_data()
    if not fms_pipeline.is_data_valid():
        await reply_to_user(message, fms_pipeline.get_user_reply_list())
        return

    await fms_pipeline.process_pipeline()
    await reply_to_user(message, fms_pipeline.get_user_reply_list())
