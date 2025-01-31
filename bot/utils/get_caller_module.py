import inspect
from typing import Optional


def get_caller_module() -> Optional[str]:
    """Получаем имя модуля, с которого был вызов функции"""
    stack = inspect.stack()
    caller_frame = stack[2]  # В вашем случае это должен быть кадр, из которого вызывается декоратор
    caller_globals = caller_frame[0].f_globals
    module_name: Optional[str] = caller_globals.get("__name__", None)
    return module_name
