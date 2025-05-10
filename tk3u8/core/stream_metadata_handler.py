import json
import re
from typing import Any
from bs4 import BeautifulSoup
from tk3u8.constants import OptionKey, Quality, StreamLink
from tk3u8.exceptions import (
    HLSLinkNotFoundError,
    InvalidQualityError,
    InvalidUsernameError,
    NoUsernameEnteredError,
    QualityNotAvailableError,
    SigiStateMissingError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    UserNotFoundError,
    UserNotLiveError,
    UserPreparingForLiveError,
    WAFChallengeError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler


class StreamMetadataHandler:
    def __init__(self, request_handler: RequestHandler, options_handler: OptionsHandler):
        self._request_handler = request_handler
        self._options_handler = options_handler
        self._source_data: dict = {}
        self._stream_data: dict = {}
        self._stream_links: dict = {}
        self._username: str | None = None
        self._quality: str | None = None

    def get_stream_link(self) -> StreamLink:
        try:
            if self._quality in self._stream_links:
                return StreamLink(self._quality, self._stream_links[self._quality])
            raise InvalidQualityError()
        except AttributeError:
            raise QualityNotAvailableError()

    def _initialize_data(self) -> None:
        if not self._username:
            new_username = self._options_handler.get_option_val(OptionKey.USERNAME)
            assert isinstance(new_username, (str, type(None)))

            if not new_username:
                raise NoUsernameEnteredError()

            self._username = new_username

        if not self._source_data:
            self._source_data = self._get_source_data()

        if not self._stream_data:
            self._stream_data = self._get_stream_data()

        if not self._stream_links:
            self._stream_links = self._get_stream_links()

        if not self._quality:
            new_quality = self._options_handler.get_option_val(OptionKey.QUALITY)
            assert isinstance(new_quality, str)
            self._quality = new_quality

    def _get_source_data(self) -> dict:
        if not self._is_username_valid(self._username):
            raise InvalidUsernameError(self._username)

        response = self._request_handler.get_data(f"https://www.tiktok.com/@{self._username}/live")

        if "Please wait..." in response.text:
            raise WAFChallengeError()

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise SigiStateMissingError()

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

    def _get_stream_links(self) -> dict:
        """
        This builds the stream links in dict. The qualities are first constructed
        into a list by getting all the values from Quality enum class except for
        the first one ("original"), as this doesn't match with the quality
        specified from the source ("origin").

        After the stream links have been added to the dict, the key "origin" is
        replaced with "original".
        """
        stream_links = {}
        qualities = [quality.value.lower() for quality in list(Quality)[1:]]
        qualities.insert(0, "origin")

        for quality in qualities:
            try:
                link = self._stream_data["data"][quality]["main"]["hls"]
            except KeyError:
                link = None

            stream_links.update({
                quality: link
            })

        stream_links["original"] = stream_links.pop("origin")

        return stream_links

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

        if status == 1:
            raise UserPreparingForLiveError(status)
        if status == 2:
            return True
        elif status == 4:
            return False
        else:
            raise UnknownStatusCodeError(status)

    def _is_link_empty(self, link: str | Any) -> bool:
        return link == "" or link is None
