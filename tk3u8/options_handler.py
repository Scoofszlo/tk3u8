from typing import Optional
import toml
from tk3u8.constants import OptionKey, Quality
from tk3u8.exceptions import FileParsingError, InvalidArgKeyError, NoUsernameEnteredError
from tk3u8.utils.paths import paths_handler


class OptionsHandler:
    def __init__(self) -> None:
        self._args: dict = {}
        self._config = self._load_config()

    def get_arg_val(self, key) -> Optional[str | int]:
        try:
            if key == OptionKey.SESSIONID_SS:
                return self._config[OptionKey.SESSIONID_SS.value]
            if key == OptionKey.TT_TARGET_IDC:
                return self._config[OptionKey.TT_TARGET_IDC.value]
            if key == OptionKey.PROXY:
                return self._args[OptionKey.PROXY.value] or self._config[OptionKey.PROXY.value]
            if key == OptionKey.USERNAME:
                try:
                    return self._args[OptionKey.USERNAME.value]
                except AttributeError:
                    raise NoUsernameEnteredError
            if key == OptionKey.QUALITY:
                if self._args[OptionKey.QUALITY.value] is not None:
                    return self._args[OptionKey.QUALITY.value]
                return Quality.ORIGINAL.value
            if key == OptionKey.WAIT_UNTIL_LIVE:
                return self._args[OptionKey.WAIT_UNTIL_LIVE.value]
            if key == OptionKey.TIMEOUT:
                return self._args[OptionKey.TIMEOUT.value]
            raise InvalidArgKeyError(key)
        except KeyError:
            return None

    def save_arg(self, arg: dict) -> None:
        self._args.update(arg)

    def _load_config(self) -> dict:
        try:
            with open(paths_handler.CONFIG_FILE_PATH, 'r') as file:
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
