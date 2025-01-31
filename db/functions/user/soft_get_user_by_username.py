from typing import Optional

from sqlalchemy.future import select

from bot.utils.handler_context import HandlerContext
from db.models.user import User


async def soft_get_user_by_id(ctx: HandlerContext, user_id: int) -> Optional[User]:
    result = await ctx.session.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()
