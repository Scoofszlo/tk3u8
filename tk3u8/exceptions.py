from tk3u8.constants import OptionKey


class RequestFailedError(Exception):
    """Custom exception for failed HTTP requests.

    Raised when an HTTP request fails due to network issues,
    invalid responses, or other related errors.
    """

    def __init__(self, exc_msg: str) -> None:
        self.message = f"Request failed: {exc_msg})"
        super().__init__(self.message)


class WAFChallengeError(Exception):
    """Custom exception when 'Please wait...' message appears when extracting data
    from source."""

    def __init__(self) -> None:
        self.message = "Source extraction failed due to WAF. Please try again later."
        super().__init__(self.message)


class SigiStateMissingError(Exception):
    """Custom exception for failed data extraction from the SIGI_STATE script tag.

    Raised when the SIGI_STATE script tag isn't found from the webpage.
    """

    def __init__(self) -> None:
        self.message = "SIGI_STATE script not found."
        super().__init__(self.message)


class UserNotLiveError(Exception):
    """Custom exception when user is not live."""

    def __init__(self, username: str) -> None:
        self.message = f"User @{username} is not live."
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Custom exception whenever data extraction from specified user fails.

    This exception will be raised whenever the account is private or the
    account doesn't exist.
    """

    def __init__(self, username: str) -> None:
        self.message = f"The user account @{username} is likely a private account, or it doesn't exist at all."
        super().__init__(self.message)


class InvalidUsernameError(Exception):
    """Custom exception whenever username entered is invalid."""

    def __init__(self, username: str) -> None:
        self.message = (
            f"The username @{username} is invalid. Ensure the username is at least "
            "2 characters long, contains only lowercase letters, numbers, underscores, "
            "and/or periods, and is up to 24 characters in length."
        )
        super().__init__(self.message)


class NoUsernameEnteredError(Exception):
    """Custom exception when no username is entered."""

    def __init__(self) -> None:
        self.message = "No username was entered. Please provide a valid username."
        super().__init__(self.message)


class UserPreparingForLiveError(Exception):
    """Custom exception when the user is preparing to go live.
    """

    def __init__(self, username: str) -> None:
        self.message = f"User @{username} is preparing to go live. Try again in a minute or two to be able to download the stream."
        super().__init__(self.message)


class UnknownStatusCodeError(Exception):
    """Custom exception whenever the status code returned isn't 2 or 4.

    This exception is a weird one, but I still implemented in case that there might be some
    situation that the status integer returns beside 2 or 4 from
    ["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]. This can be useful
    for debugging if TikTok made some changes in their end.
    """

    def __init__(self, status_code: int) -> None:
        self.message = f"Invalid status code. (Status code: {status_code} {type(status_code)})"
        super().__init__(self.message)


class InvalidQualityError(Exception):
    """Custom exception when quality arg is incorrectly entered."""

    def __init__(self) -> None:
        self.message = "Invalid video quality entered. Supported args: [-q {original,uhd,hd,ld,sd}])"
        super().__init__(self.message)


class QualityNotAvailableError(Exception):
    """Custom exception when quality is not available for download."""

    def __init__(self) -> None:
        self.message = "The requested video quality is not available for download."
        super().__init__(self.message)


class LinkNotAvailableError(Exception):
    """Custom exception when the stream link isn't available for some reason."""

    def __init__(self) -> None:
        self.message = "Stream link can't be retrieved. Please try again."
        super().__init__(self.message)


class StreamDataNotFoundError(Exception):
    """Custom exception when the stream data can't be scraped."""

    def __init__(self, username: str) -> None:
        self.message = f"Stream data can't be retrieved from user @{username}. Please try again."
        super().__init__(self.message)


class LiveStatusCodeNotFoundError(Exception):
    """Custom exception when the live status code failed to be retrieved."""

    def __init__(self, username: str) -> None:
        self.message = f"Live status code could not be retrieved from user @{username}."
        super().__init__(self.message)


class HLSLinkNotFoundError(Exception):
    """Custom exception when the HLS stream link isn't available, even though
    there is a stream going on."""

    def __init__(self, username: str) -> None:
        self.message = f"HLS stream link not found for user @{username}."
        super().__init__(self.message)


class HLSLinkTemporarilyUnavailableError(Exception):
    """Custom exception when the HLS stream link isn't available temporarily
    for some reason.

    The difference with the exception 'HLSLinkNotFoundError' is that this exception
    will be used if the HLS link becomes unavaiable initially, but becomes available
    again whenever user retries to download the live stream. The other exception is
    only used if there is no actually available HLS stream links persistently.
    """

    def __init__(self) -> None:
        self.message = "Cannot proceed with downloading as the stream link was somehow unavailable during stream data extraction. Try downloading again."
        super().__init__(self.message)


class InvalidArgKeyError(Exception):
    """Custom exception when an invalid key is encountered."""

    def __init__(self, key: OptionKey) -> None:
        self.message = f"The key '{key}' is invalid or not recognized."
        super().__init__(self.message)


class FileParsingError(Exception):
    """Custom exception for when there is a problem parsing the file."""

    def __init__(self) -> None:
        self.message = "Error parsing config file."
        super().__init__(self.message)


class InvalidCookieError(Exception):
    """Custom exception when user improperly sets cookie in the config file."""

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DownloadError(Exception):
    """Custom exception when there is an issue downloading with yt-dlp."""

    def __init__(self, e: Exception) -> None:
        super().__init__(f"Download failed with error: {e}")


class InvalidExtractorError(Exception):
    """Custom exception raised when an invalid extractor is used."""

    def __init__(self) -> None:
        super().__init__("The specified extractor is invalid or has failed.")
