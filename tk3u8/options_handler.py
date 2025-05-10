from typing import Optional
import toml
from tk3u8.constants import OptionKey
from tk3u8.exceptions import FileParsingError, InvalidArgKeyError
from tk3u8.path_initializer import PathInitializer


class OptionsHandler:
    def __init__(self) -> None:
        self._paths_initializer = PathInitializer()
        self._args_values: dict = {}
        self._config_values: dict = self._load_config_values()

    def get_option_val(self, key) -> Optional[str | int]:
        try:
            key_map = {
                OptionKey.SESSIONID_SS: lambda: self._config_values[OptionKey.SESSIONID_SS.value],
                OptionKey.TT_TARGET_IDC: lambda: self._config_values[OptionKey.TT_TARGET_IDC.value],
                OptionKey.PROXY: lambda: self._args_values[OptionKey.PROXY.value] or self._config_values[OptionKey.PROXY.value],
                OptionKey.USERNAME: lambda: self._args_values[OptionKey.USERNAME.value],
                OptionKey.QUALITY: lambda: self._args_values[OptionKey.QUALITY.value.lower()],
                OptionKey.WAIT_UNTIL_LIVE: lambda: self._args_values[OptionKey.WAIT_UNTIL_LIVE.value],
                OptionKey.TIMEOUT: lambda: self._args_values[OptionKey.TIMEOUT.value],
            }
            if key in key_map:
                return key_map[key]()
            raise InvalidArgKeyError(key)
        except KeyError:
            return None

    def save_args_values(self, *args, **kwargs) -> None:
        for arg in args:
            if isinstance(arg, dict):
                self._args_values.update(arg)
            else:
                raise TypeError(f"Argument {arg} is not a dict.")

        for key, value in kwargs.items():
            for option_key in list(OptionKey):
                if key in option_key.value:
                    self._args_values.update({key: value})

    def _load_config_values(self) -> dict:
        try:
            with open(self._paths_initializer.CONFIG_FILE_PATH, 'r') as file:
                config = self._retouch_config_values(toml.load(file))
                return config
        except FileNotFoundError:
            raise FileParsingError()

    def _retouch_config_values(self, config: dict) -> dict:
        """Turns empty strings into None values"""

        raw_config: dict = config['config']

        for key, value in raw_config.items():
            if value == "":
                raw_config[key] = None

        return raw_config
