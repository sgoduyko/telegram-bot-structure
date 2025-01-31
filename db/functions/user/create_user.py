from typing import Optional

from sqlalchemy.exc import IntegrityError

from bot.utils.handler_context import HandlerContext
from db.models.user import User


async def create_user(ctx: HandlerContext, username: str) -> Optional[User]:
    savepoint = await ctx.session.begin_nested()
    try:
        user = User(username=username)
        ctx.session.add(user)
        await savepoint.commit()
    except IntegrityError:
        await savepoint.rollback()  # подчищаем до savepoint и продолжаем спокойно работать
        return None
    return user
