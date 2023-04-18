import traceback
from typing import Optional

from loguru import logger


class MyException(Exception):
    message = '系统错误'
    status = 400

    def __init__(self, message: Optional[str] = None, status: Optional[int] = None):
        if not message:
            logger.warning(traceback.format_exc())
        self.message = message or self.message
        self.status = status or self.status

    def __str__(self):
        return self.message
