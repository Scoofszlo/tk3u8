import logging
from tk3u8.core.model import Tk3u8


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


__all__ = [
    "Tk3u8"
]
