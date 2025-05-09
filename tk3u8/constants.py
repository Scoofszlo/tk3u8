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
    UHD_60 = "UHD_60"
    UHD = "UHD"
    HD_60 = "HD_60"
    HD = "HD"
    LD = "LD"
    SD = "SD"


class OptionKey(Enum):
    SESSIONID_SS = "sessionid_ss"
    TT_TARGET_IDC = "tt-target-idc"
    PROXY = "proxy"
    USERNAME = "username"
    QUALITY = "quality"
    WAIT_UNTIL_LIVE = "wait_until_live"
    TIMEOUT = "timeout"


# Default configuration settings
DEFAULT_CONFIG = {
    "config": {
        "sessionid_ss": "",
        "tt-target-idc": "",
        "proxy": ""
    }
}
