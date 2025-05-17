import re
from typing import Any
from tk3u8.exceptions import UnknownStatusCodeError, UserPreparingForLiveError


def is_username_valid(username) -> bool:
    pattern = r"^[a-z0-9_.]{2,24}$"
    match = re.match(pattern, username)

    if match:
        return True
    return False


def is_user_exists(source_data: dict) -> bool:
    if source_data.get("LiveRoom"):
        return True
    return False


def is_user_live(source_data: dict) -> bool:
    status = source_data["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]

    if status == 1:
        raise UserPreparingForLiveError(status)
    if status == 2:
        return True
    elif status == 4:
        return False
    else:
        raise UnknownStatusCodeError(status)


def _is_link_empty(link: str | Any) -> bool:
    return link == "" or link is None
