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


# Default user agent
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
    "Mozilla/5.0 (X11; Linux i686; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
]
