from typing import List
from tk3u8.constants import OptionKey, StreamLink
from tk3u8.core.extractor import APIExtractor, Extractor, WebpageExtractor
from tk3u8.core.helper import is_user_exists, is_user_live, is_username_valid
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


class StreamMetadataHandler:
    def __init__(self, request_handler: RequestHandler, options_handler: OptionsHandler):
        self._request_handler = request_handler
        self._options_handler = options_handler
        self._extractor_classes: List[type[Extractor]] = [APIExtractor, WebpageExtractor]
        self._source_data: dict = {}
        self._stream_data: dict = {}
        self._stream_links: dict = {}
        self._live_status_code: int | None = None
        self._username: str | None = None
        self._quality: str | None = None

    def get_stream_link(self) -> StreamLink:
        assert isinstance(self._quality, str)

        try:
            if self._quality in self._stream_links:
                return StreamLink(self._quality, self._stream_links[self._quality])
            raise InvalidQualityError()
        except AttributeError:
            raise QualityNotAvailableError()

    def initialize_data(self) -> None:
        self._process_data()

    def update_data(self) -> None:
        self._process_data()

    def _get_username(self) -> str:
        username = self._options_handler.get_option_val(OptionKey.USERNAME)
        assert isinstance(username, (str, type(None)))

        if not username:
            raise NoUsernameEnteredError()

        if not is_username_valid(username):
            raise InvalidUsernameError(username)

        return username

    def _process_data(self) -> None:
        if not self._username:
            self._username = self._get_username()

        for idx, extractor_class in enumerate(self._extractor_classes):
            try:
                extractor = extractor_class(self._username, self._request_handler)

                self._source_data = self._get_and_validate_source_data(extractor, extractor_class)
                self._live_status_code = extractor.get_live_status_code(self._source_data)

                if not is_user_live(self._live_status_code):
                    break

                self._stream_data = extractor.get_stream_data(self._source_data)
                self._stream_links = extractor.get_stream_links(self._stream_data)
                self._quality = self._get_and_validate_quality()

                break
            except (
                WAFChallengeError,
                SigiStateMissingError,
                StreamDataNotFoundError,
                HLSLinkNotFoundError
            ) as e:
                if idx != len(self._extractor_classes) - 1:
                    print(f"Extractor #{idx+1} ({extractor.__class__.__name__}) failed due to {type(e).__name__}. Trying next extractor method (Extractor #{idx+2})")
                else:
                    print(f"Extractor #{idx+1} ({extractor.__class__.__name__}) failed due to {type(e).__name__}. No more extractors to be used. The program will now exit.")
                    exit()

    def _get_and_validate_source_data(self, extractor: Extractor, extractor_class: type[Extractor]) -> dict:
        source_data: dict = extractor.get_source_data()

        if not is_user_exists(extractor_class, source_data):
            raise UserNotFoundError(self._username)

        return source_data

    def _get_and_validate_quality(self) -> str:
        quality = self._options_handler.get_option_val(OptionKey.QUALITY)
        assert isinstance(quality, str)

        return quality
