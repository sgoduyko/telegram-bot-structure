import logging
import os
import re

from bot.const.const import (
    DEV_ENV_NAME,
    LOCAL_ENV_NAME,
    PRODUCTION_ENV_NAME,
    ROOT_DIR,
    STAGE_ENV_NAME,
    TEST_ENV_NAME,
)
from bot.const.types import TPathToDir

if not (BOT_API := os.getenv("BOT_API")):
    raise ValueError("Bot api key is not set")

if not (BOT_HASH := os.getenv("BOT_HASH")):
    raise ValueError("Bot hash is not set")

if not (BOT_TOKEN := os.getenv("BOT_TOKEN")):
    raise ValueError("Bot token is not set")


ENVIRONMENT = os.getenv("ENVIRONMENT", LOCAL_ENV_NAME)
if not ENVIRONMENT in (LOCAL_ENV_NAME, DEV_ENV_NAME, TEST_ENV_NAME, STAGE_ENV_NAME, PRODUCTION_ENV_NAME):
    raise ValueError(f"Invalid environment value - {ENVIRONMENT}")

IS_DEBUG_MODE = bool(os.getenv("DEBUG", False) == "TRUE")


REDIS_FMS_DATA_DELIMITER = "__"
REDIS_OPERATION_DELIMITER = "___"

USERNAME_REGEX = r"^[a-zA-Z0-9_]{4,15}$"
USERNAME_PATTERN = re.compile(USERNAME_REGEX)

PINCODE_REGEX = r"^[0-9]{5}$"
PINCODE_PATTERN = re.compile(PINCODE_REGEX)

CHECK_FMS_PIPELINE_CALLING_ORDER = False if ENVIRONMENT in ("PRODUCTION", "STAGE") else True


if ENVIRONMENT in (PRODUCTION_ENV_NAME, STAGE_ENV_NAME):
    LOGGING_LEVEL = logging.ERROR
else:
    LOGGING_LEVEL = logging.INFO

if IS_DEBUG_MODE:
    LOGGING_LEVEL = logging.DEBUG


if ENVIRONMENT == LOCAL_ENV_NAME:
    # Для локальной машине пишем логи для человека
    IS_LOG_FORMATE_AS_JSON = False
else:
    # на окружении пишем для системы мониторинга
    IS_LOG_FORMATE_AS_JSON = True


if ENVIRONMENT == LOCAL_ENV_NAME:
    IS_WRITE_IN_CONSOLE_MODE = True
else:
    IS_WRITE_IN_CONSOLE_MODE = True


LOG_FILE_NAME = "telegram_bot.log"
LOG_DIR_PATH: TPathToDir = TPathToDir(os.path.join(ROOT_DIR, "logs"))
