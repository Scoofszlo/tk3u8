from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class DownloadLink:
    quality: "Quality"
    link: Optional[str]


class StatusCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    FORBIDDEN = 403
    UNAUTHORIZED = 401
    SERVER_ERROR = 500
    GATEWAY_TIMEOUT = 504
    SERVICE_UNAVAILABLE = 503


class Quality(Enum):
    ORIGINAL = "Original"
    UHD = "UHD"
    HD = "HD"
    LD = "LD"
    SD = "SD"


class Mode(Enum):
    AUTO = "Auto"
    MANUAL = "Manual"


STREAM_DATA_DIR = "user_data/stream_data.json"
