import pytest
from unittest.mock import MagicMock, mock_open, patch
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.constants import LiveStatus, OptionKey, StreamLink
from tk3u8.exceptions import InvalidQualityError
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler


MOCK_CONFIG = {
    OptionKey.SESSIONID_SS.value: "sessid",
    OptionKey.TT_TARGET_IDC.value: None,
    OptionKey.PROXY.value: None,
    OptionKey.WAIT_UNTIL_LIVE.value: False,
    OptionKey.TIMEOUT.value: 30,
    OptionKey.FORCE_REDOWNLOAD.value: False
}

LOADED_MOCK_CONFIG = {
    "config": MOCK_CONFIG
}


@pytest.fixture
def options_handler():
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG), \
         patch("tk3u8.options_handler.PathsHandler") as mock_path_init:
        mock_path_init.return_value.CONFIG_FILE_PATH = "dummy_path"

        handler = OptionsHandler()

        return handler


@pytest.fixture
def request_handler(options_handler):
    return RequestHandler(options_handler)


def test_initialization_sets_dependencies(request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    assert handler._request_handler is request_handler
    assert handler._options_handler is options_handler


def test_initialize_data_success(monkeypatch, request_handler, options_handler):
    class MockExtractor:
        def __init__(self, username, request_handler):
            pass

        def get_source_data(self):
            return {'mock': 'data'}

        def get_live_status(self, source_data):
            return LiveStatus.LIVE

        def get_stream_data(self, source_data):
            return {'data': {'original': {'main': {'hls': 'http://mock'}}}}

        def get_stream_links(self, stream_data):
            return {'original': 'http://mock'}

    handler = StreamMetadataHandler(request_handler, options_handler)
    handler._extractor_classes = [MockExtractor]
    handler._get_and_validate_source_data = lambda extractor, extractor_class: {'mock': 'data'}
    handler.initialize_data('testuser')
    assert handler._username == 'testuser'
    assert handler._live_status == LiveStatus.LIVE
    assert handler._stream_links == {'original': 'http://mock'}
    assert handler._stream_data == {'data': {'original': {'main': {'hls': 'http://mock'}}}}


def test_get_username_returns_correct_value(request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    handler._username = 'abc'
    assert handler.get_username() == 'abc'


def test_get_live_status_returns_correct_value(request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)

    handler._live_status = LiveStatus.LIVE
    assert handler.get_live_status() == LiveStatus.LIVE

    handler._live_status = LiveStatus.OFFLINE
    assert handler.get_live_status() == LiveStatus.OFFLINE

    handler._live_status = LiveStatus.PREPARING_TO_GO_LIVE
    assert handler.get_live_status() == LiveStatus.PREPARING_TO_GO_LIVE


def test_get_stream_link_returns_link_by_codec(request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    handler._stream_links = {
        "original": {
            "h264": "http://testh264",
            "h265": "http://testh265"
        }
    }
    handler._username = "testuser"

    # Test for H.265
    link = handler.get_stream_link('original', use_h265=True)
    assert isinstance(link, StreamLink)
    assert link.quality == 'original'
    assert link.link == 'http://testh265'

    link = handler.get_stream_link('original', use_h265=False)
    assert link.link == 'http://testh264'


def test_get_stream_link_invalid_quality_raises(request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    handler._stream_links = {'original': 'http://test'}
    with pytest.raises(InvalidQualityError):
        handler.get_stream_link('origgg', use_h265=True)


def test_validate_username_empty_exits(monkeypatch, request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    with patch('tk3u8.core.stream_metadata_handler.exit', side_effect=SystemExit):
        with pytest.raises(SystemExit):
            handler._validate_username('')


def test_validate_username_invalid_exits(monkeypatch, request_handler, options_handler):
    handler = StreamMetadataHandler(request_handler, options_handler)
    with patch('tk3u8.core.stream_metadata_handler.exit', side_effect=SystemExit):
        with pytest.raises(SystemExit):
            handler._validate_username('bad!user')


def test_get_and_validate_source_data_user_not_exists(monkeypatch, request_handler, options_handler):
    """Tests whether the program exits whenever that the user doesn't exist
    from the API/webpage extraction."""
    handler = StreamMetadataHandler(request_handler, options_handler)
    handler._username = "abc"
    extractor = MagicMock()
    extractor_class = MagicMock()
    monkeypatch.setattr('tk3u8.core.stream_metadata_handler.is_user_exists', lambda c, d: False)
    monkeypatch.setattr('tk3u8.core.stream_metadata_handler.console.print', lambda *a, **k: None)
    with patch('tk3u8.core.stream_metadata_handler.exit', side_effect=SystemExit):
        with pytest.raises(SystemExit):
            handler._get_and_validate_source_data(extractor, extractor_class)
