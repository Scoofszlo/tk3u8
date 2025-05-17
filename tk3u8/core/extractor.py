from abc import abstractmethod
import json

from bs4 import BeautifulSoup

from tk3u8.constants import Quality
from tk3u8.core import helper as hlp
from tk3u8.exceptions import HLSLinkNotFoundError, InvalidUsernameError, SigiStateMissingError, StreamDataNotFoundError, UserNotFoundError, UserNotLiveError, WAFChallengeError
from tk3u8.session.request_handler import RequestHandler


class Extractor:
    def __init__(self, username: str, request_handler: RequestHandler):
        self._request_handler = request_handler
        self._username = username

    @abstractmethod
    def get_source_data(self):
        pass

    @abstractmethod
    def get_stream_data(self):
        pass

    @abstractmethod
    def get_stream_links(self, stream_data: dict) -> dict:
        """
        This builds the stream links in dict. The qualities are first constructed
        into a list by getting all the values from Quality enum class except for
        the first one ("original"), as this doesn't match with the quality
        specified from the source ("origin").

        After the stream links have been added to the dict, the key "origin" is
        replaced with "original".
        """
        stream_links = {}
        qualities = [quality.value for quality in list(Quality)[1:]]
        qualities.insert(0, "origin")

        for quality in qualities:
            try:
                link = stream_data["data"][quality]["main"]["hls"]
            except KeyError:
                link = None

            # Link can be an empty string. Based on my testing, this errpr
            # will most likely to happen for those who live in the US region.
            if link == "":
                raise HLSLinkNotFoundError(self._username)

            stream_links.update({
                quality: link
            })

        stream_links["original"] = stream_links.pop("origin")

        return stream_links


class WebpageExtractor(Extractor):
    def get_source_data(self) -> dict:
        if not hlp.is_username_valid(self._username):
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

    def get_stream_data(self, source_data: dict):
        if not hlp.is_user_exists(source_data):
            raise UserNotFoundError(self._username)

        if not hlp.is_user_live(source_data):
            raise UserNotLiveError(self._username)

        try:
            return json.loads(source_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self._username)
