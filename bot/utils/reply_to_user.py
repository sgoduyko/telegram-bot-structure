from typing import List

from pyrogram.types import Message

from bot.const.types import TReplyToUserText


async def reply_to_user(message: Message, reply_list: List[TReplyToUserText]) -> None:
    """
    Отправим пользователю ответы, которые мы собрали в процессе работы
    :param message: Обьект сообщения пользователя
    :param reply_list: список сообщений, которые нам нужно отправить пользователю как ответ
    """
    if not reply_list:
        return

    if len(reply_list) == 1:
        # ну случай, если можно обойти без цикла
        await message.reply(reply_list[0])
        return

    for msg in reply_list:
        await message.reply(msg)
