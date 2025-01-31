import logging
import os
from pathlib import Path

from bot.config import (
    BOT_API,
    BOT_HASH,
    BOT_TOKEN,
    ENVIRONMENT,
    IS_DEBUG_MODE,
    LOG_DIR_PATH,
    LOGGING_LEVEL,
)
from bot.const.const import SESSION_NAME, TEMP_DIR
from bot.const.types import TPathToDir
from bot.utils.custom_logger import setup_root_logger
from bot.utils.app_bot_runner import AppConfig, AppRunner

if os.getenv("ISRUNFROMLOCAL"):
    logging.info("uploaded environment variables for local environment")
    from dotenv import load_dotenv

    load_dotenv()

logging.info(f"ENVIRONMENT = {ENVIRONMENT}")
logging.info(f"IS_DEBUG_MODE = {IS_DEBUG_MODE}")
logging.info(f"LOGGING_LEVEL = {logging.getLevelName(LOGGING_LEVEL)}")

Path(TEMP_DIR).mkdir(parents=True, exist_ok=True)
Path(LOG_DIR_PATH).mkdir(parents=True, exist_ok=True)
setup_root_logger(LOGGING_LEVEL)

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
