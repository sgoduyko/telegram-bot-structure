import logging
from typing import Optional

from bot.utils.handler_context import HandlerContext
from db.models.user import User


async def update_user_pincode(ctx: HandlerContext, user: Optional[User], pincode: int) -> None:
    """
    Обновление пароля пользователя
    :param ctx: HandlerContext обьект
    :param user: User обьект
    :param pincode: новый пинкод
    :return:
    """
    if user is None:
        logging.error("Registration. Update pincode function. User is null.", extra=ctx.get_logging_extra())
        raise Exception("Registration. Update pincode function. User is null.")
    user.pincode = pincode
    ctx.session.add(user)
    await ctx.session.commit()
