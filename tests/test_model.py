import pytest
from unittest.mock import patch

from tk3u8.constants import OptionKey
from tk3u8.core.model import Tk3u8


@pytest.fixture
def tk3u8():
    return Tk3u8(program_data_dir=None)


def test_set_proxy_updates_option_and_request_handler(tk3u8):
    with patch.object(tk3u8._options_handler, 'save_args_values') as mock_save_args, \
         patch.object(tk3u8._options_handler, 'get_option_val', return_value='http://proxy:8080') as mock_get_option, \
         patch.object(tk3u8._request_handler, 'update_proxy') as mock_update_proxy:
        proxy = 'http://proxy:8080'
        tk3u8.set_proxy(proxy)
        mock_save_args.assert_called_once()
        mock_get_option.assert_called_once()
        mock_update_proxy.assert_called_once_with('http://proxy:8080')


def test_set_cookies_updates_option_and_request_handler(tk3u8):
    cookies = {
        'sessionid_ss': 'abc123',
        'tt_target_idc': 'idc456'
    }
    tk3u8.set_cookies(cookies)

    set_sessionid_ss = cookies.get(OptionKey.SESSIONID_SS.value)
    set_tt_target_idc = cookies.get("tt-target-idc")
    stored_sessionid_ss = tk3u8._request_handler._session.cookies.get(OptionKey.SESSIONID_SS.value)
    stored_tt_target_idc = tk3u8._request_handler._session.cookies.get(OptionKey.TT_TARGET_IDC.value)

    assert set_sessionid_ss == stored_sessionid_ss
    assert set_tt_target_idc == stored_tt_target_idc


def test_download_triggers_all_components(tk3u8):
    with patch.object(tk3u8._options_handler, 'save_args_values') as mock_save_args, \
         patch.object(tk3u8._stream_metadata_handler, 'initialize_data') as mock_init_data, \
         patch.object(tk3u8._downloader, 'download') as mock_download:
        tk3u8.download('testuser', quality='original', wait_until_live=True, timeout=10, force_redownload=False, use_h265=True)
        mock_save_args.assert_called_once_with(
            wait_until_live=True, timeout=10, force_redownload=False, use_h265=True
        )
        mock_init_data.assert_called_once_with('testuser')
        mock_download.assert_called_once_with('original')
