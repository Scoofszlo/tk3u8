from argparse import Namespace
import toml
from tk3u8.constants import CONFIG_FILE_PATH, OptionKey, Quality
from tk3u8.exceptions import FileParsingError, NoUsernameEnteredError


class OptionsHandler:
    def __init__(self, args: Namespace | None = None):
        self.script_args = {}
        self.cl_args: Namespace = args if args else Namespace()
        self.config = self._load_config()

    def get_option_val(self, key) -> str | None:
        try:
            if key == OptionKey.SESSIONID_SS:
                return self.config[OptionKey.SESSIONID_SS.value]
            if key == OptionKey.TT_TARGET_IDC:
                return self.config[OptionKey.TT_TARGET_IDC.value]
            if key == OptionKey.PROXY:
                return self.script_args[OptionKey.PROXY.value] or self.cl_args.proxy or self.config[OptionKey.PROXY.value]
            if key == OptionKey.USERNAME:
                try:
                    return self.script_args[OptionKey.USERNAME.value] or self.cl_args.username
                except AttributeError:
                    raise NoUsernameEnteredError
            if key == OptionKey.QUALITY:
                try:
                    return self.script_args[OptionKey.QUALITY.value].lower() or self.cl_args.quality
                except AttributeError:
                    return Quality.ORIGINAL.value.lower()
            if key == OptionKey.WAIT_UNTIL_LIVE:
                return self.script_args[OptionKey.WAIT_UNTIL_LIVE.value]
            if key == OptionKey.TIMEOUT:
                return self.script_args[OptionKey.TIMEOUT.value]
            return None
        except KeyError:
            return None

    def save_script_args(
            self,
            username: str | None,
            quality: Quality | None,
            wait_until_live: bool,
            timeout: int
        ):
        self.script_args[OptionKey.USERNAME.value] = username
        self.script_args[OptionKey.QUALITY.value] = quality.value if quality else None
        self.script_args[OptionKey.WAIT_UNTIL_LIVE.value] = wait_until_live
        self.script_args[OptionKey.TIMEOUT.value] = timeout

    def _load_config(self) -> dict:
        try:
            with open(CONFIG_FILE_PATH, 'r') as file:
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
