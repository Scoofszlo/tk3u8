import pytest
from unittest.mock import patch, mock_open
from tk3u8.constants import OptionKey
from tk3u8.options_handler import OptionsHandler
from tk3u8.paths_handler import PathsHandler


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
def mock_paths_handler():
    return PathsHandler()


def test_load_config_and_defaults(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)
        assert handler._config_values[OptionKey.SESSIONID_SS.value] == "sessid"
        assert handler._config_values[OptionKey.TT_TARGET_IDC.value] is None
        assert handler._config_values[OptionKey.PROXY.value] is None
        assert handler._config_values[OptionKey.WAIT_UNTIL_LIVE.value] is False


def test_get_option_val_precedence(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)

        # Not set in args, should get from config
        assert handler.get_option_val(OptionKey.SESSIONID_SS) == "sessid"

        # Not set in args or config, should get default
        assert handler.get_option_val(OptionKey.QUALITY) is None

        # Set in args, should override config
        handler.save_args_values({OptionKey.SESSIONID_SS.value: "override"})
        assert handler.get_option_val(OptionKey.SESSIONID_SS) == "override"


def test_save_args_values_and_type_error(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)
        with pytest.raises(TypeError):
            handler.save_args_values("not a dict")


def test_file_not_found_raises(mock_paths_handler):
    with patch("tk3u8.options_handler.open", side_effect=FileNotFoundError):
        with pytest.raises(SystemExit):
            OptionsHandler(mock_paths_handler)


def test_save_args_overwrites_previous(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)

        handler.save_args_values({OptionKey.USERNAME.value: "user1"})
        assert handler.get_option_val(OptionKey.USERNAME) == "user1"

        handler.save_args_values({OptionKey.USERNAME.value: "user2"})
        assert handler.get_option_val(OptionKey.USERNAME) == "user2"


def test_get_option_val_returns_none_for_missing(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)

        # Needed to pop the _config_values as the SESSIONID_SS from mockup
        # config contains a value
        handler._config_values.pop(OptionKey.SESSIONID_SS.value)
        assert handler.get_option_val(OptionKey.SESSIONID_SS) is None


def test_get_option_val_args_override_config(mock_paths_handler):
    with patch("tk3u8.options_handler.open", mock_open(read_data="dummy")), \
         patch("tk3u8.options_handler.toml.load", return_value=LOADED_MOCK_CONFIG):
        handler = OptionsHandler(mock_paths_handler)
        handler.save_args_values({OptionKey.PROXY.value: "127.0.0.1:8080"})
        assert handler.get_option_val(OptionKey.PROXY) == "127.0.0.1:8080"
        handler.save_args_values({OptionKey.PROXY.value: "0.0.0.1:1111"})
        assert handler.get_option_val(OptionKey.PROXY) == "0.0.0.1:1111"
