import asyncio
import dataclasses
import importlib.util
import logging
import os
import sys
from typing import List, Optional, Type

from pyrogram.client import Client
from pyrogram.handlers.callback_query_handler import CallbackQueryHandler
from pyrogram.handlers.chat_join_request_handler import ChatJoinRequestHandler
from pyrogram.handlers.chat_member_updated_handler import ChatMemberUpdatedHandler
from pyrogram.handlers.chosen_inline_result_handler import ChosenInlineResultHandler
from pyrogram.handlers.deleted_messages_handler import DeletedMessagesHandler
from pyrogram.handlers.disconnect_handler import DisconnectHandler
from pyrogram.handlers.edited_message_handler import EditedMessageHandler
from pyrogram.handlers.handler import Handler
from pyrogram.handlers.inline_query_handler import InlineQueryHandler
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.handlers.poll_handler import PollHandler
from pyrogram.handlers.raw_update_handler import RawUpdateHandler
from pyrogram.handlers.user_status_handler import UserStatusHandler

from bot.bot_menu import BOT_COMMANDS
from bot.const.const import HANDLERS_DIR, HANDLERS_LIST_VAR_NAME
from bot.const.dataclasses import HandlerObj
from bot.utils.add_handler_context import add_handler_context
from bot.utils.list_modules_in_directory import list_modules_in_directory

EXCLUDE_DIR_NAMES = {"__pycache__"}

HandlerType = Type[Handler]


@dataclasses.dataclass
class AppConfig:
    bot_api: str
    bot_hash: str
    bot_token: str
    session_name: str


class AppRunner:
    def __init__(self, conf: AppConfig) -> None:
        self.conf = conf
        app = Client(conf.session_name, api_id=conf.bot_api, api_hash=conf.bot_hash, bot_token=conf.bot_token)
        self.app: Client = app
        self.handlers_list: List[HandlerObj] = []

    def collect_handlers(self) -> None:
        logging.info(f"class {self.__class__.__name__}. Collecting handlers start.")
        modules = list_modules_in_directory([], HANDLERS_DIR)

        handlers_list = []
        for module_abs_path in set(modules):
            module_name = os.path.splitext(os.path.basename(module_abs_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, os.path.join(module_name, module_abs_path))
            logging.debug(f"made spec for module {module_name}")
            if spec is None:
                logging.warning("Spec didn't create for path {}".format(module_abs_path))
                continue
            if spec.loader is None:
                logging.warning(f"For spec {spec} the loader is None")
                continue

            module = importlib.util.module_from_spec(spec)
            logging.debug(f"made module obj {module}")
            module.__dict__[HANDLERS_LIST_VAR_NAME] = []
            logging.debug(f"added list for handlers in module {module}")
            sys.modules[module_name] = module
            spec.loader.exec_module(module)  # При запуске модуля все обработчики записываются в список
            logging.debug(f"module {module} loaded . handlers list={module.__dict__[HANDLERS_LIST_VAR_NAME]}")
            handlers_list.extend(module.__dict__[HANDLERS_LIST_VAR_NAME])

            del module.__dict__[HANDLERS_LIST_VAR_NAME]
            del sys.modules[module_name]

        self.handlers_list = handlers_list
        self.handlers_collected = True
        logging.info(f"class {self.__class__.__name__}. Collecting handlers completed.")

    @staticmethod
    def get_handler_by_func_name(func_name: str) -> Optional[HandlerType]:
        for prefix, handler in (
            ("callback_query_", CallbackQueryHandler),
            ("chat_join_request_", ChatJoinRequestHandler),
            ("chat_member_updated_", ChatMemberUpdatedHandler),
            ("chose_inline_result_", ChosenInlineResultHandler),
            ("deleted_messages_", DeletedMessagesHandler),
            ("disconnect_", DisconnectHandler),
            ("edited_message_", EditedMessageHandler),
            ("inline_query_", InlineQueryHandler),
            ("message_", MessageHandler),
            ("poll_", PollHandler),
            ("raw_update_", RawUpdateHandler),
            ("user_status_", UserStatusHandler),
        ):
            if func_name.startswith(prefix):
                return handler
        return None

    def upload_handlers(self) -> None:
        logging.info(f"class {self.__class__.__name__}. Uploading handlers start.")
        if not getattr(self, "handlers_collected", False):
            logging.error("handlers didn't be collected")
            raise Exception("Handlers not collected")

        for handler_obj in sorted(self.handlers_list, key=lambda item: item.register_number):
            handler_callback = self.get_handler_by_func_name(handler_obj.handler_name)
            if handler_callback is None:
                logging.error(f"Didn't fund handler for func {handler_obj.handler_name}")
                continue
            func_call = add_handler_context(handler_obj.func)

            if not handler_obj.filters:
                self.app.add_handler(handler_callback(func_call))
            else:
                self.app.add_handler(handler_callback(func_call, handler_obj.filters))

            logging.debug(f"handler added for func {handler_obj.handler_name}")

        logging.info(f"class {self.__class__.__name__}. Uploading handlers completed.")

    async def start(self) -> None:
        await self.app.start()

    async def add_menu(self) -> None:
        await self.app.set_bot_commands(BOT_COMMANDS)

    async def running_pipeline(self) -> None:
        await self.start()
        await self.add_menu()
        self.collect_handlers()
        self.upload_handlers()
        await asyncio.Event().wait()

    def run(self) -> None:
        self.app.run(self.running_pipeline())
