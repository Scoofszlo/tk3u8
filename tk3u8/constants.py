from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class StreamLink:
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


class Cookie(Enum):
    SESSIONID_SS = "sessionid_ss",
    TT_TARGET_IDC = "tt-target-idc"


PROGRAM_DATA_DIR = "user_data"
STREAM_DATA_DIR = PROGRAM_DATA_DIR + "/stream_data.json"
CONFIG_FILE_PATH = PROGRAM_DATA_DIR + "/config.toml"

# Default configuration settings
DEFAULT_CONFIG = {
    "config": {
        "sessionid_ss": "",
        "tt-target-idc": "",
    }
}
