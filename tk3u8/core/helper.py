import re
from tk3u8.core.extractor import APIExtractor, Extractor, WebpageExtractor
from tk3u8.exceptions import InvalidExtractorError, UnknownStatusCodeError, UserPreparingForLiveError


def is_username_valid(username) -> bool:
    pattern = r"^[a-z0-9_.]{2,24}$"
    match = re.match(pattern, username)

    if match:
        return True
    return False


def is_user_exists(extractor: type[Extractor], source_data: dict) -> bool:
    if extractor == WebpageExtractor:
        if source_data.get("LiveRoom"):
            return True
        return False

    elif extractor == APIExtractor:
        message = source_data["message"]
        if message == "user_not_found":
            return False
        return True

    else:
        raise InvalidExtractorError()


def is_user_live(status_code: int) -> bool:
    if status_code == 1:
        raise UserPreparingForLiveError(status_code)
    elif status_code == 2:
        return True
    elif status_code == 4:
        return False
    else:
        raise UnknownStatusCodeError(status_code)
