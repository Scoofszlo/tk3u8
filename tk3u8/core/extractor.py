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

    def get_stream_links(self, stream_data: dict[str, dict]) -> dict:
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

        for quality_key in qualities:
            quality_dict = {}

            for vid_format in stream_data.keys():
                try:
                    link = stream_data[vid_format]["data"][quality_key]["main"]["hls"]
                except KeyError:
                    link = None

                quality_dict.update({
                    vid_format: link
                })

            stream_links.update({
                quality_key: quality_dict
            })

        stream_links["original"] = stream_links.pop("origin")

        are_stream_links_empty = self._are_hls_stream_links_empty(stream_links)
        if are_stream_links_empty:
            logger.exception(f"{HLSLinkNotFoundError.__name__}: {HLSLinkNotFoundError(self._username)}")
            raise HLSLinkNotFoundError(self._username)

        logger.debug(messages.retrieved_stream_links.format(
            username=self._username,
            stream_links=json.dumps(stream_links, indent=4, ensure_ascii=False)
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

    def _are_hls_stream_links_empty(self, stream_links: dict[str, dict[str, str | None]]) -> bool:
        """
        Checks whether the all stream links contain similar empty strings.
        If satisfied, this function returns True and vice versa.

        This is important because there is a tendency that stream links can be empty.
        Based on testing, this is more likely to happen if you and the user you are
        trying to download is in different server locations.
        """

        h264_bool: bool = False
        h265_bool: bool = False

        for quality in stream_links:
            links_by_codec = stream_links[quality]

            for codec, link in links_by_codec.items():
                if link != "":
                    continue
                else:
                    if codec == "h264":
                        h264_bool = True
                    elif codec == "h265":
                        h265_bool = True

        return all([h264_bool, h265_bool])


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
            stream_data = {
                "h264": json.loads(source_data["data"]["liveRoom"]["streamData"]["pull_data"]["stream_data"]),
                "h265": json.loads(source_data["data"]["liveRoom"]["hevcStreamData"]["pull_data"]["stream_data"])
            }

            logger.debug(messages.extracted_stream_data.format(
                username=self._username,
                stream_data=json.dumps(stream_data, indent=4, ensure_ascii=False)
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
            stream_data = {
                "h264": json.loads(source_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"]),
                "h265": json.loads(source_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["hevcStreamData"]["pull_data"]["stream_data"])
            }

            logger.debug(messages.extracted_stream_data.format(
                username=self._username,
                stream_data=json.dumps(stream_data, indent=4, ensure_ascii=False)
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
