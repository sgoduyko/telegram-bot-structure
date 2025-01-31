import logging

from bot.modules.fms_data_pipeline import fms_pool
from bot.utils.expections import UnExpectedLineException
from bot.utils.handler_context import HandlerContext


async def reply_by_fms_state(ctx: HandlerContext, prefix_msg: str = "") -> None:
    if not ctx.fms_name:
        logging.error("check if fms is exist must to be before the function", extra=ctx.get_logging_extra())
        raise UnExpectedLineException("check if fms is exist must to be before the function")

    fms_pipeline = fms_pool.get_pipeline(ctx.fms_name)(ctx)
    await ctx.message.reply(f"{prefix_msg}{fms_pipeline.fms.get_reply_text_for_current_state()}")
    return
