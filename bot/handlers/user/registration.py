import logging

from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery

from bot.const import handlers_order
from bot.const.const import (
    INTERNAL_ERROR_TEXT,
    REGISTRATION_FMS_NAME,
)
from bot.modules.fms_data_pipeline.registration import SighInFMSDataPipeline
from bot.utils.add_handler_with_filters import add_handler_with_filters
from bot.utils.handler_context import HandlerContext
from bot.utils.is_correct_target_fms import is_correct_target_fms
from bot.utils.reply_by_fms_state import reply_by_fms_state
from bot.utils.reply_to_user import reply_to_user


@add_handler_with_filters(order=handlers_order.CALLBACK_REGISTRATION__ORDER_NUMBER, filters=filters.regex(r"^registration"))
async def callback_query_registration(ctx: HandlerContext, client: Client, call: CallbackQuery) -> None:
    await call.answer()
    if not is_correct_target_fms(REGISTRATION_FMS_NAME, ctx.fms_name):
        msg = "У вас есть незавершенный процесс. Наша система не позволяет работать с двумя процессами одновременно."
        await ctx.message.reply(msg)
        await reply_by_fms_state(ctx)
        return

    if ctx.fms_name and ctx.fms_name == REGISTRATION_FMS_NAME:
        await ctx.message.reply("Вы уже находите в процессе создания пользователя. ")
        await reply_by_fms_state(ctx)
        return

    if ctx.user:
        await ctx.message.reply(
            "На данный момент вы уже вошли в системы. " "Для создания пользователя вам нужно сперва выйти с помощью команды /logout"
        )
        return

    if ctx.fms_name:
        logging.error(
            f"При вызове команды /login пользователь незалогинен" f" и при этом есть незавершенный процесс, чего не может быть.",
            extra=ctx.get_logging_extra(),
        )
        await ctx.message.reply(INTERNAL_ERROR_TEXT)
        return

    fms_pipeline = SighInFMSDataPipeline(ctx)
    await fms_pipeline.init_data()
    fms_pipeline.validate_data()
    if not fms_pipeline.is_data_valid():
        await reply_to_user(ctx.message, fms_pipeline.get_user_reply_list())
        return

    await fms_pipeline.process_pipeline()
    await reply_to_user(ctx.message, fms_pipeline.get_user_reply_list())
    await call.answer()
