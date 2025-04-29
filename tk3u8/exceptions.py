class AutoModeError(Exception):
    """Custom exception whenever users attempts to use auto mode.

    This exception will be removed once the implementation of this method
    is done
    """

    def __init__(self) -> None:
        self.message = "Auto mode is not yet available."
        super().__init__(self.message)


class RequestFailedError(Exception):
    """Custom exception for failed HTTP requests.

    Raised when an HTTP request fails due to network issues,
    invalid responses, or other related errors.
    """

    def __init__(self, status_code: int) -> None:
        self.message = f" Request failed with status code: {status_code})"
        super().__init__(self.message)


class ScriptTagNotFoundError(Exception):
    """Custom exception for failed data extraction from the script tag

    Raised when the SIGI_STATE script tag isn't found from the webpage
    """

    def __init__(self) -> None:
        self.message = "SIGI_STATE script not found"
        super().__init__(self.message)


class UserNotLiveError(Exception):
    """Custom exception when user is not live"""

    def __init__(self, username) -> None:
        self.message = f"User @{username} is not live."
        super().__init__(self.message)


class UserNotFoundError(Exception):
    """Custom exception whenever data extraction from specified user fails.

    This exception will be raised whenever the account is private or the
    account doesn't exist
    """

    def __init__(self, username) -> None:
        self.message = f"The user account @{username} is likely a private account, or it doesn't exist at all."
        super().__init__(self.message)


class InvalidUsernameError(Exception):
    """Custom exception whenever username entered is invalid."""

    def __init__(self, username) -> None:
        self.message = f"The username @{username} is invalid. Ensure the username contains only lowercase letters, numbers, underscores, and/or periods, and is up to 24 characters in length."
        super().__init__(self.message)


class NoUsernameEnteredError(Exception):
    """Custom exception when no username is entered."""

    def __init__(self) -> None:
        self.message = "No username was entered. Please provide a valid username."
        super().__init__(self.message)


class UnknownStatusCodeError(Exception):
    """Custom exception whenever the status code returned isn't 2 or 4.

    This exception is a weird one, but I still implemented in case that there might be some
    situation that the status integer returns beside 2 or 4 from
    ["LiveRoom"]["liveRoomUserInfo"]["user"]["status"].This can be useful
    for debugging if TikTok made some changes in their end.
    """

    def __init__(self, status) -> None:
        self.message = f"Invalid status. (Status: {status} {type(status)})"
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

    def __init__(self, username) -> None:
        self.message = f"Stream data can't be retrieved from user @{username}. Please try again."
        super().__init__(self.message)


class InvalidArgKeyError(Exception):
    """Custom exception when an invalid key is encountered."""

    def __init__(self, key) -> None:
        self.message = f"The key '{key}' is invalid or not recognized."
        super().__init__(self.message)


class FileParsingError(Exception):
    """Custom exception for when there is a problem parsing the file"""

    def __init__(self) -> None:
        self.message = "Error parsing config file."
        super().__init__(self.message)


class InvalidCookieError(Exception):
    """Custom exception when user improperly sets cookie in the config file"""

    def __init__(self, message) -> None:
        super().__init__(message)


class DownloadError(Exception):
    """Custom exception when there is an issue downloading with yt-dlp."""

    def __init__(self, e) -> None:
        super().__init__(f"Download failed with error: {e}")
