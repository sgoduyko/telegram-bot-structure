from bot.enums.base import FMSStateBaseEnum


class SighInStateEnum(FMSStateBaseEnum):
    not_sighin_user = "initializing_value"
    username = "enter_username"
    pincode = "enter_pincode"
