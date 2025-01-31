import os

from bot.const.types import TEnvName, TFMSName, TPathToDir, TReplyToUserMessage

USERNAME_REQUIREMENTS_TEXT: TReplyToUserMessage = TReplyToUserMessage(
    """Никней должен быть от 4 до 15 символов и может состоять из:
 1) латинских символов нижнего и верхнего регистра
 2) нижнее подчеркивание"""
)

PINCODE_REQUIREMENTS_TEXT: TReplyToUserMessage = TReplyToUserMessage("Пинкод должен состоять из 5 цифр")
REGISTRATION_UNEXPECTED_LINE_ERR_TEXT: TReplyToUserMessage = TReplyToUserMessage("Регистрация пользователя. Необработанный случай.")

INTERNAL_ERROR_TEXT: TReplyToUserMessage = TReplyToUserMessage("Что-то пошло не так...Уже пытаемся понять причину.")

REGISTRATION_FMS_NAME: TFMSName = TFMSName("registration")

LOG_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

ROOT_DIR: TPathToDir = TPathToDir(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))  # telegram_bot/
HANDLERS_DIR: TPathToDir = TPathToDir(os.path.join(ROOT_DIR, "bot", "handlers"))
TEMP_DIR: TPathToDir = TPathToDir(os.path.join(ROOT_DIR, "temp"))

HANDLERS_LIST_VAR_NAME: str = "handlers_list"
SESSION_NAME: str = "telegram_bot"

LOCAL_ENV_NAME: TEnvName = TEnvName("LOCAL")
DEV_ENV_NAME: TEnvName = TEnvName("DEV")
TEST_ENV_NAME: TEnvName = TEnvName("TEST")
STAGE_ENV_NAME: TEnvName = TEnvName("TEST")
PRODUCTION_ENV_NAME: TEnvName = TEnvName("PRODUCTION")
