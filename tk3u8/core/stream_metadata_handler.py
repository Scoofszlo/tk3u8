import json
import re
from bs4 import BeautifulSoup
from tk3u8.constants import OptionKey, Quality, StreamLink
from tk3u8.exceptions import InvalidQualityError, InvalidUsernameError, NoUsernameEnteredError, QualityNotAvailableError, SourceDataExtractionError, StreamDataNotFoundError, UnknownStatusCodeError, UserNotFoundError, UserNotLiveError
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler


class StreamMetadataHandler:
    def __init__(self, request_handler: RequestHandler, options_handler: OptionsHandler):
        self._request_handler = request_handler
        self._options_handler = options_handler
        self._source_data: dict = {}
        self._stream_data: dict = {}
        self._username: str | None = None
        self._quality: str | None = None

    def _initialize_data(self) -> None:
        if not self._username:
            new_username = self._options_handler.get_arg_val(OptionKey.USERNAME)
            assert isinstance(new_username, (str, type(None)))

            if not new_username:
                raise NoUsernameEnteredError()

            self._username = new_username

        if not self._source_data:
            self._source_data = self._get_source_data()

        if not self._stream_data:
            self._stream_data = self._get_stream_data()

        if not self._quality:
            new_quality = self._options_handler.get_arg_val(OptionKey.QUALITY)
            assert isinstance(new_quality, str)
            self._quality = new_quality

    def _get_source_data(self) -> dict:
        if not self._is_username_valid(self._username):
            raise InvalidUsernameError(self._username)

        response = self._request_handler.get_data(self._username)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise SourceDataExtractionError()

        script_content = script_tag.text
        return json.loads(script_content)

    def _get_stream_data(self) -> dict:
        if not self._is_user_exists():
            raise UserNotFoundError(self._username)

        if not self.is_user_live():
            raise UserNotLiveError(self._username)

        try:
            return json.loads(self._source_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self._username)

    def get_stream_link(self) -> StreamLink:
        try:
            if self._quality == Quality.ORIGINAL.value.lower():
                return StreamLink(Quality.ORIGINAL, self._stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
            else:
                for quality in list(Quality)[1:]:  # Turns them into a list of its members and skips the first one since it is already checked from the if statement
                    if quality.value.lower() == self._quality:
                        return StreamLink(quality, self._stream_data.get("data", None).get(self._quality, None).get("main", None).get("hls", None))

            raise InvalidQualityError()
        except AttributeError:
            raise QualityNotAvailableError()

    def _update_data(self) -> None:
        self._source_data = self._get_source_data()
        self._stream_data = self._get_stream_data()

    def _is_username_valid(self, username) -> bool:
        pattern = r"^[a-z0-9_.]{2,24}$"
        match = re.match(pattern, username)

        if match:
            return True
        return False

    def _is_user_exists(self) -> bool:
        if self._source_data.get("LiveRoom"):
            return True
        return False

    def is_user_live(self) -> bool:
        status = self._source_data["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]

        if status == 2:
            return True
        elif status == 4:
            return False
        else:
            raise UnknownStatusCodeError(status)
