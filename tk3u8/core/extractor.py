from abc import ABC, abstractmethod
import json

from bs4 import BeautifulSoup

from tk3u8.constants import LiveStatus, Quality
from tk3u8.exceptions import (
    HLSLinkNotFoundError,
    LiveStatusCodeNotFoundError,
    SigiStateMissingError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    WAFChallengeError
)
from tk3u8.messages import messages
from tk3u8.session.request_handler import RequestHandler
import logging


logger = logging.getLogger(__name__)


class Extractor(ABC):
    """
    Abstract base class for extracting streaming data for a given username.
    Subclasses must implement methods to fetch source data and extract stream data.
    """

    def __init__(self, username: str, request_handler: RequestHandler):
        self._request_handler = request_handler
        self._username = username

    @abstractmethod
    def get_source_data(self) -> dict:
        """Fetch the raw source data for the user."""

    @abstractmethod
    def get_stream_data(self, source_data: dict) -> dict:
        """Gets the stream data from the extracted source data."""

    @abstractmethod
    def get_live_status(self, source_data: dict) -> LiveStatus:
        """
        Gets the live status code from the extracted source data, then returns
        a LiveStatus constant.
        """

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
                logger.exception(f"{HLSLinkNotFoundError.__name__}: {HLSLinkNotFoundError(self._username)}")
                raise HLSLinkNotFoundError(self._username)

            stream_links.update({
                quality: link
            })

        stream_links["original"] = stream_links.pop("origin")

        logger.debug(messages.retrieved_stream_links.format(
            username=self._username,
            stream_links=stream_links
        ))

        return stream_links

    def _get_live_status(self, status_code: int) -> LiveStatus:
        if status_code == 1:
            return LiveStatus.PREPARING_TO_GO_LIVE
        elif status_code == 2:
            return LiveStatus.LIVE
        elif status_code == 4:
            return LiveStatus.OFFLINE
        else:
            logger.exception(f"{UnknownStatusCodeError.__name__}: {UnknownStatusCodeError(status_code)}")
            raise UnknownStatusCodeError(status_code)


class APIExtractor(Extractor):
    def get_source_data(self) -> dict:
        response = self._request_handler.get_data(f"https://www.tiktok.com/api-live/user/room?aid=1988&sourceType=54&uniqueId={self._username}")

        soup = BeautifulSoup(response.text, "html.parser")
        content = json.loads(soup.text)

        logger.debug(messages.fetched_content.format(
            username=self._username,
            content=content
        ))

        return content

    def get_stream_data(self, source_data: dict) -> dict:
        try:
            stream_data = json.loads(source_data["data"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
            logger.debug(messages.extracted_stream_data.format(
                username=self._username,
                stream_data=stream_data
            ))

            return stream_data
        except KeyError:
            logger.exception(f"{StreamDataNotFoundError.__name__}: {StreamDataNotFoundError(self._username)}")
            raise StreamDataNotFoundError(self._username)

    def get_live_status(self, source_data: dict) -> LiveStatus:
        try:
            status_code = source_data["data"]["user"]["status"]
            logger.debug(messages.extracted_status_code.format(
                username=self._username,
                status_code=status_code
            ))

            return self._get_live_status(status_code)
        except KeyError:
            logger.exception(f"{LiveStatusCodeNotFoundError.__name__}: {LiveStatusCodeNotFoundError(self._username)}")
            raise LiveStatusCodeNotFoundError(self._username)


class WebpageExtractor(Extractor):
    def get_source_data(self) -> dict:
        response = self._request_handler.get_data(f"https://www.tiktok.com/@{self._username}/live")

        if "Please wait..." in response.text:
            logger.exception(f"{WAFChallengeError.__name__}: {WAFChallengeError}")
            raise WAFChallengeError()

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            logger.exception(f"{SigiStateMissingError.__name__}: {SigiStateMissingError}")
            raise SigiStateMissingError()

        content = json.loads(script_tag.text)

        logger.debug(messages.fetched_content.format(
            username=self._username,
            content=content
        ))

        return content

    def get_stream_data(self, source_data: dict) -> dict:
        try:
            stream_data = json.loads(source_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
            logger.debug(messages.extracted_stream_data.format(
                username=self._username,
                stream_data=stream_data
            ))

            return stream_data
        except KeyError:
            logger.exception(f"{StreamDataNotFoundError.__name__}: {StreamDataNotFoundError(self._username)}")
            raise StreamDataNotFoundError(self._username)

    def get_live_status(self, source_data: dict) -> LiveStatus:
        try:
            status_code = source_data["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]
            logger.debug(messages.extracted_status_code.format(
                username=self._username,
                status_code=status_code
            ))

            return self._get_live_status(status_code)
        except KeyError:
            logger.exception(f"{LiveStatusCodeNotFoundError.__name__}: {LiveStatusCodeNotFoundError(self._username)}")
            raise LiveStatusCodeNotFoundError(self._username)
