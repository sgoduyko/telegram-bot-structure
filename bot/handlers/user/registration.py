from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import CallbackQuery

from bot.const import handlers_order
from bot.const.const import REGISTRATION_FMS_NAME
from bot.modules.fms_data_pipeline.registration import SighInFMSDataPipeline
from bot.utils.add_handler_with_filters import add_handler_with_filters
from bot.utils.get_fms_data_for_sighin import get_fms_data_for_registration
from bot.utils.handler_context import HandlerContext
from bot.utils.reply_to_user import reply_to_user


@add_handler_with_filters(order=handlers_order.CALLBACK_REGISTRATION__ORDER_NUMBER, filters=filters.regex(r"^registration"))
async def callback_query_registration(ctx: HandlerContext, client: Client, call: CallbackQuery) -> None:
    fms_name, fms_data = await get_fms_data_for_registration(ctx.telegram_user_id)

    if fms_name and fms_name != REGISTRATION_FMS_NAME:
        await ctx.message.reply("Регистрация вам не требуется)")
        return

    fms_manager = SighInFMSDataPipeline(ctx, fms_data)
    await fms_manager.init_data()
    fms_manager.validate_data()
    if not fms_manager.is_data_valid():
        await reply_to_user(ctx.message, fms_manager.get_user_reply_list())
        return

    await fms_manager.process_pipeline()
    await reply_to_user(ctx.message, fms_manager.get_user_reply_list())
    await call.answer()
