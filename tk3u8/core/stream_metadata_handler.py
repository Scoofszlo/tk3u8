import logging
from typing import List, Optional
from tk3u8.constants import LiveStatus, StreamLink
from tk3u8.cli.console import console
from tk3u8.core.extractor import APIExtractor, Extractor, WebpageExtractor
from tk3u8.core.helper import is_user_exists, is_username_valid
from tk3u8.exceptions import (
    HLSLinkNotFoundError,
    HLSLinkTemporarilyUnavailableError,
    InvalidQualityError,
    InvalidUsernameError,
    NoUsernameEnteredError,
    QualityNotAvailableError,
    SigiStateMissingError,
    StreamDataNotFoundError,
    UserNotFoundError,
    WAFChallengeError
)
from tk3u8.messages import messages
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler


logger = logging.getLogger(__name__)


class StreamMetadataHandler:
    """
    Handles the retrieval, validation, and management of stream metadata for a given user.
    This class coordinates the extraction of stream data from multiple sources (API, webpage, etc.),
    validates user input, manages live status, and provides access to stream links and metadata.
    It uses a list of extractor classes to attempt data retrieval in sequence, handling errors and
    falling back as needed.

    Attributes:
        _request_handler (RequestHandler): Handles HTTP requests for data extraction.
        _options_handler (OptionsHandler): Manages configuration options.
        _extractor_classes (List[type[Extractor]]): List of extractor classes to use for data retrieval.
        _source_data (dict): Raw data obtained from the extractor.
        _stream_data (dict): Processed stream data.
        _stream_links (dict): Available stream links by quality.
        _live_status (LiveStatus | None): Current live status of the stream.
        _username (str | None): Username for which metadata is being handled.
    """
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
        with console.status(messages.processing_data):
            self._process_data(username)

    def update_data(self) -> None:
        with console.status(messages.processing_data):
            self._process_data()

    def get_username(self) -> str:
        assert isinstance(self._username, str)

        return self._username

    def get_live_status(self) -> LiveStatus:
        assert isinstance(self._live_status, LiveStatus)

        return self._live_status

    def get_stream_link(self, quality: str, use_h265: bool) -> StreamLink:
        try:
            if quality in self._stream_links:
                assert isinstance(self._username, str)
                codec, formatted_codec_str = ("h265", "H.265") if use_h265 else ("h264", "H.264")
                stream_link = self._stream_links[quality][codec]

                if stream_link == "":
                    logger.exception(f"{HLSLinkTemporarilyUnavailableError.__name__}: {HLSLinkTemporarilyUnavailableError()}")
                    console.print(messages.empty_stream_link_error)
                    exit(0)

                stream_link_obj = StreamLink(quality, stream_link)
                logger.debug(f"Chosen stream link: {stream_link_obj} ({formatted_codec_str})")

                return stream_link_obj

            logger.exception(f"{InvalidQualityError.__name__}: {InvalidQualityError}")
            raise InvalidQualityError()
        except AttributeError:
            logger.exception(f"{QualityNotAvailableError.__name__}: {QualityNotAvailableError}")
            raise QualityNotAvailableError()

    def _process_data(self, username: Optional[str] = None) -> None:
        """
        Processes stream metadata for the given username.

        Whenever the first extractor fails due to the given exceptions, the next
        available extractor will be used. When all of the available extractors
        failed, the program will exit.
        """
        if username:
            self._username = self._validate_username(username)

        assert isinstance(self._username, str)
        logger.debug(messages.processing_data_for_user.format(username=self._username))

        for idx, extractor_class in enumerate(self._extractor_classes):
            logger.debug(messages.trying_extractor.format(
                pos=idx + 1,
                extractor_class_name=extractor_class.__name__
            ))

            try:
                extractor = extractor_class(self._username, self._request_handler)

                self._source_data = self._get_and_validate_source_data(extractor, extractor_class)
                self._live_status = extractor.get_live_status(self._source_data)

                if self._live_status in (LiveStatus.OFFLINE, LiveStatus.PREPARING_TO_GO_LIVE):
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
                    error_msg = messages.current_extractor_failed.format(
                        current_extr_pos=idx + 1,
                        current_extr_name=extractor.__class__.__name__,
                        exc_name=type(e).__name__,
                        next_extr_pos=idx + 2
                    )
                    console.print(error_msg)
                    logger.error(error_msg)
                else:
                    error_msg = messages.last_extractor_failed.format(
                        current_extr_pos=idx + 1,
                        current_extr_name=extractor.__class__.__name__,
                        exc_name=type(e).__name__,
                    )
                    console.print(error_msg)
                    logger.error(error_msg)
                    exit()

    def _validate_username(self, username: str) -> str:
        if not username:
            logger.exception(f"{NoUsernameEnteredError.__name__}: {NoUsernameEnteredError()}")
            console.print(messages.no_username_entered)
            exit(0)

        if not is_username_valid(username):
            logger.exception(f"{InvalidUsernameError.__name__}: {InvalidUsernameError(username)}")
            console.print(messages.invalid_username.format(username=username))
            exit(0)

        logger.debug(f"Entered username: {username}")

        return username

    def _get_and_validate_source_data(self, extractor: Extractor, extractor_class: type[Extractor]) -> dict:
        source_data: dict = extractor.get_source_data()

        assert isinstance(self._username, str)

        if not is_user_exists(extractor_class, source_data):
            logger.exception(f"{UserNotFoundError.__name__}: {UserNotFoundError(self._username)}")
            console.print(messages.account_not_found.format(username=self._username))
            exit(0)

        return source_data
