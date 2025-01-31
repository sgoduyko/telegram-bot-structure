from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from bot.const import handlers_order
from bot.utils.add_handler_with_filters import add_handler_with_filters
from bot.utils.handler_context import HandlerContext
from redis_db.client import redis_session


@add_handler_with_filters(order=handlers_order.COMMAND_LOGIN__ORDER_NUMBER, filters=filters.command("login"))
async def message_login(ctx: HandlerContext, client: Client, message: Message) -> None:
    if ctx.user:
        await message.reply_text("Вы уже вошли в систему. Воспользуйтесь нашим меню работы с задачами /tasks")
        return

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton("Вход", callback_data="login"), InlineKeyboardButton("Регистрация", callback_data="registration/")]
        ]
    )
    await message.reply("Какой-нибудь текст", reply_markup=markup)


@add_handler_with_filters(order=handlers_order.COMMAND_LOGOUT__ORDER_NUMBER, filters=filters.command("logout"))
async def message_logout(ctx: HandlerContext, client: Client, message: Message) -> None:
    is_key_exist = bool(await redis_session.delete(str(message.from_user.id)))
    if is_key_exist:
        await message.reply("Вы вышли из системы")
        return
    await message.reply("У вас нет активной сессии")
