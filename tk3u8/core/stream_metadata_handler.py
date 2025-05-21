from tk3u8.constants import OptionKey, StreamLink
from tk3u8.core.extractor import APIExtractor, WebpageExtractor
from tk3u8.exceptions import (
    HLSLinkNotFoundError,
    InvalidQualityError,
    NoUsernameEnteredError,
    QualityNotAvailableError,
    SigiStateMissingError,
    StreamDataNotFoundError,
    WAFChallengeError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler


class StreamMetadataHandler:
    def __init__(self, request_handler: RequestHandler, options_handler: OptionsHandler):
        self._request_handler = request_handler
        self._options_handler = options_handler
        self._extractor_classes = [APIExtractor, WebpageExtractor]
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
        if not self._username:
            new_username = self._options_handler.get_option_val(OptionKey.USERNAME)
            assert isinstance(new_username, (str, type(None)))

            if not new_username:
                raise NoUsernameEnteredError()

            self._username = new_username

        for idx, extractor_class in enumerate(self._extractor_classes):
            try:
                extractor = extractor_class(self._username, self._request_handler)

                self._source_data = extractor.get_source_data()
                self._stream_data = extractor.get_stream_data(self._source_data)
                self._live_status_code = extractor.get_live_status_code(self._source_data)
                self._stream_links = extractor.get_stream_links(self._stream_data)

                new_quality = self._options_handler.get_option_val(OptionKey.QUALITY)
                assert isinstance(new_quality, str)
                self._quality = new_quality

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

    def update_data(self) -> None:
        assert isinstance(self._username, str)

        for extractor_class in self._extractor_classes:
            extractor = extractor_class(self._username, self._request_handler)

            self._source_data = extractor.get_source_data()
            self._stream_data = extractor.get_stream_data(self._source_data)
            self._live_status_code = extractor.get_live_status_code(self._source_data)
