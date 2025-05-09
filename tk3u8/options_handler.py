from typing import Optional
import toml
from tk3u8.constants import OptionKey
from tk3u8.exceptions import FileParsingError, InvalidArgKeyError
from tk3u8.utils.paths import PathsHandler


class OptionsHandler:
    def __init__(self) -> None:
        self.paths_handler = PathsHandler()
        self._args: dict = {}
        self._config: dict = self._load_config()

    def get_arg_val(self, key) -> Optional[str | int]:
        try:
            if key == OptionKey.SESSIONID_SS:
                return self._config[OptionKey.SESSIONID_SS.value]
            if key == OptionKey.TT_TARGET_IDC:
                return self._config[OptionKey.TT_TARGET_IDC.value]
            if key == OptionKey.PROXY:
                return self._args[OptionKey.PROXY.value] or self._config[OptionKey.PROXY.value]
            if key == OptionKey.USERNAME:
                return self._args[OptionKey.USERNAME.value]
            if key == OptionKey.QUALITY:
                return self._args[OptionKey.QUALITY.value.lower()]
            if key == OptionKey.WAIT_UNTIL_LIVE:
                return self._args[OptionKey.WAIT_UNTIL_LIVE.value]
            if key == OptionKey.TIMEOUT:
                return self._args[OptionKey.TIMEOUT.value]
            raise InvalidArgKeyError(key)
        except KeyError:
            return None

    def save_args(self, *args, **kwargs) -> None:
        for arg in args:
            if isinstance(arg, dict):
                self._args.update(arg)
            else:
                raise TypeError(f"Argument {arg} is not a dict.")

        for key, value in kwargs.items():
            for option_key in list(OptionKey):
                if key in option_key.value:
                    self._args.update({key: value})

    def _load_config(self) -> dict:
        try:
            with open(self.paths_handler.CONFIG_FILE_PATH, 'r') as file:
                config = self._retouch_config(toml.load(file))
                return config
        except FileNotFoundError:
            raise FileParsingError()

    def _retouch_config(self, config: dict) -> dict:
        """Turns empty strings into None values"""

        raw_config: dict = config['config']

        for key, value in raw_config.items():
            if value == "":
                raw_config[key] = None

        return raw_config
