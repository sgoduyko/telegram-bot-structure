import logging
import os
from typing import List

from bot.const.types import TModuleAbsPath, TPathToDir


def list_modules_in_directory(modules: List[TModuleAbsPath], directory: TPathToDir) -> List[TModuleAbsPath]:
    logging.debug("function list_modules_in_directory start")
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".py") and file_name != "__init__.py":
                modules.append(TModuleAbsPath(os.path.join(root, file_name)))

    logging.debug(f"function list_modules_in_directory result={modules}")
    return modules
