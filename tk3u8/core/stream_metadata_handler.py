import logging
from typing import List, Optional
from tk3u8.constants import LiveStatus, StreamLink
from tk3u8.cli.console import console
from tk3u8.core.extractor import APIExtractor, Extractor, WebpageExtractor
from tk3u8.core.helper import is_user_exists, is_username_valid
from tk3u8.exceptions import (
    HLSLinkNotFoundError,
    InvalidQualityError,
    InvalidUsernameError,
    NoUsernameEnteredError,
    QualityNotAvailableError,
    SigiStateMissingError,
    StreamDataNotFoundError,
    UserNotFoundError,
    WAFChallengeError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler


logger = logging.getLogger(__name__)


class StreamMetadataHandler:
    def __init__(self, request_handler: RequestHandler, options_handler: OptionsHandler):
        self._request_handler = request_handler
        self._options_handler = options_handler
        self._extractor_classes: List[type[Extractor]] = [APIExtractor, WebpageExtractor]
        self._source_data: dict = {}
        self._stream_data: dict = {}
        self._stream_links: dict = {}
        self._live_status: LiveStatus | None = None
        self._username: str | None = None

    def initialize_data(self, username: str) -> None:
        with console.status("Processing data..."):
            self._process_data(username)

    def update_data(self) -> None:
        self._process_data()

    def get_username(self) -> str:
        assert isinstance(self._username, str)

        return self._username

    def get_live_status(self) -> LiveStatus:
        assert isinstance(self._live_status, LiveStatus)

        return self._live_status

    def get_stream_link(self, quality: str) -> StreamLink:
        try:
            if quality in self._stream_links:
                stream_link = StreamLink(quality, self._stream_links[quality])
                logger.debug(f"Chosen stream link: {stream_link}")

                return stream_link
            logger.exception(f"{InvalidQualityError.__name__}: {InvalidQualityError}")
            raise InvalidQualityError()
        except AttributeError:
            logger.exception(f"{QualityNotAvailableError.__name__}: {QualityNotAvailableError}")
            raise QualityNotAvailableError()

    def _process_data(self, username: Optional[str] = None):
        if username:
            self._username = self._validate_username(username)

        assert isinstance(self._username, str)
        logger.debug(f"Processing data for user @{self._username}")

        for idx, extractor_class in enumerate(self._extractor_classes):
            logger.debug(f"Trying extractor #{idx+1}: {extractor_class.__name__}")

            try:
                extractor = extractor_class(self._username, self._request_handler)

                self._source_data = self._get_and_validate_source_data(extractor, extractor_class)
                self._live_status = extractor.get_live_status(self._source_data)

                if self._live_status in (LiveStatus.OFFLINE, LiveStatus.PREPARING_TO_GO_LIVE):
                    logger.debug(f"User @{self._username} is not live (status: {self._live_status}). Stopping extraction")
                    break

                self._stream_data = extractor.get_stream_data(self._source_data)
                self._stream_links = extractor.get_stream_links(self._stream_data)

                break
            except (
                WAFChallengeError,
                SigiStateMissingError,
                StreamDataNotFoundError,
                HLSLinkNotFoundError
            ) as e:
                if idx != len(self._extractor_classes) - 1:
                    error_msg = f"Extractor #{idx+1} ({extractor.__class__.__name__}) failed due to {type(e).__name__}. Trying next extractor method (Extractor #{idx+2})"
                    print(error_msg)
                    logger.error(error_msg)
                else:
                    error_msg = f"Extractor #{idx+1} ({extractor.__class__.__name__}) failed due to {type(e).__name__}. No more extractors to be used. The program will now exit."
                    print(error_msg)
                    logger.error(error_msg)
                    exit()

    def _validate_username(self, username: str) -> str:
        if not username:
            logger.exception(f"{NoUsernameEnteredError.__name__}: {NoUsernameEnteredError()}")
            raise NoUsernameEnteredError()

        if not is_username_valid(username):
            logger.exception(f"{InvalidUsernameError.__name__}: {InvalidUsernameError(username)}")
            raise InvalidUsernameError(username)

        logger.debug(f"Entered username: {username}")

        return username

    def _get_and_validate_source_data(self, extractor: Extractor, extractor_class: type[Extractor]) -> dict:
        source_data: dict = extractor.get_source_data()

        if not is_user_exists(extractor_class, source_data):
            logger.exception(f"{UserNotFoundError.__name__}: {UserNotFoundError(self._username)}")
            raise UserNotFoundError(self._username)

        return source_data
