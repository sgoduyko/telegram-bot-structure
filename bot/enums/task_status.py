from bot.enums.base import FMSStateBaseEnum


class TaskStatus(FMSStateBaseEnum):
    draft = "DRAFT"
    in_progress = "IN_PROGRESS"
    closed = "CLOSED"
