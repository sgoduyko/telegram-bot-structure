import logging
import os
from pathlib import Path

from bot.config import (
    BOT_API,
    BOT_HASH,
    BOT_TOKEN,
    CHECK_FMS_PIPELINE_CALLING_ORDER,
    ENVIRONMENT,
    IS_DEBUG_MODE,
    LOG_DIR_PATH,
    LOGGING_LEVEL,
    STRONG_CHECK_TYPING,
)
from bot.const.const import SESSION_NAME, TEMP_DIR
from bot.const.types import TPathToDir
from bot.utils.app_bot_runner import AppConfig, AppRunner
from bot.utils.custom_logger import setup_root_logger

Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)
setup_root_logger(LOGGING_LEVEL)

if os.getenv("ISRUNFROMLOCAL"):
    logging.info("ENVIRONMENT VARIABLES UPLOADED FROM .env FILE")
    from dotenv import load_dotenv

    load_dotenv()


logging.info(f"ENVIRONMENT = {ENVIRONMENT}")
logging.info(f"IS_DEBUG_MODE = {IS_DEBUG_MODE}")
logging.info(f"LOGGING_LEVEL = {logging.getLevelName(LOGGING_LEVEL)}")
logging.info(f"CHECK_FMS_PIPELINE_CALLING_ORDER = {CHECK_FMS_PIPELINE_CALLING_ORDER}")
logging.info(f"STRONG_CHECK_TYPING = {STRONG_CHECK_TYPING}")


if __name__ == "__main__":
    session_path: TPathToDir = TPathToDir(os.path.join(TEMP_DIR, SESSION_NAME))
    config = AppConfig(
        bot_api=str(BOT_API),
        bot_hash=str(BOT_HASH),
        bot_token=str(BOT_TOKEN),
        session_name=str(session_path),
    )
    app_runner = AppRunner(config)
    app_runner.run()
