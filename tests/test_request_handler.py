import pytest
from unittest.mock import MagicMock, mock_open, patch
from tk3u8.options_handler import OptionsHandler
from tk3u8.session.request_handler import RequestHandler
from tk3u8.constants import USER_AGENT_LIST, OptionKey
from tk3u8.exceptions import RequestFailedError


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
def mock_options_handler():
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG), \
         patch("tk3u8.options_handler.PathInitializer") as mock_path_init:
        mock_path_init.return_value.CONFIG_FILE_PATH = "dummy_path"

        handler = OptionsHandler()

        return handler


@pytest.fixture
def mock_session(monkeypatch):
    with patch('tk3u8.session.request_handler.requests.Session') as mock_sess_cls:
        yield mock_sess_cls


def test_init_sets_cookies_and_user_agent(mock_options_handler, mock_session):
    mock_sess = MagicMock()
    mock_session.return_value = mock_sess
    RequestHandler(mock_options_handler)

    # Cookies set
    assert mock_sess.cookies.update.call_count == 1

    # User-Agent set
    assert mock_sess.headers.update.call_count == 1

    ua = mock_sess.headers.update.call_args[0][0]["User-Agent"]
    assert ua in USER_AGENT_LIST


def test_get_data_success(mock_options_handler, mock_session):
    mock_sess = MagicMock()
    mock_resp = MagicMock()

    mock_resp.status_code = 200
    mock_sess.get.return_value = mock_resp
    mock_session.return_value = mock_sess
    handler = RequestHandler(mock_options_handler)
    resp = handler.get_data('http://test')
    assert resp is mock_resp
    mock_sess.get.assert_called_once_with('http://test')


def test_get_data_failure_raises(mock_options_handler, mock_session):
    mock_sess = MagicMock()
    mock_resp = MagicMock()

    mock_resp.status_code = 404
    mock_sess.get.return_value = mock_resp
    mock_session.return_value = mock_sess

    handler = RequestHandler(mock_options_handler)
    with pytest.raises(RequestFailedError) as exc:
        handler.get_data('http://fail')
    assert '404' in str(exc.value)


def test_update_proxy_sets_proxies(mock_options_handler, mock_session):
    mock_sess = MagicMock()
    mock_session.return_value = mock_sess

    handler = RequestHandler(mock_options_handler)
    handler.update_proxy('http://proxy:8080')
    assert mock_sess.proxies.update.called
    assert mock_sess.proxies.update.call_args[0][0]["http"] == 'http://proxy:8080'
    assert mock_sess.proxies.update.call_args[0][0]["https"] == 'http://proxy:8080'
