import os
import toml
from tk3u8.constants import PROGRAM_DATA_DIR, OptionKey, Quality
from tk3u8.exceptions import FileParsingError, InvalidArgKeyError, NoUsernameEnteredError


class OptionsHandler:
    def __init__(self):
        self.args = {}
        self.PROGRAM_DATA_DIR = PROGRAM_DATA_DIR
        self.CONFIG_PATH = PROGRAM_DATA_DIR + "/config.toml"
        self.config = self._load_config()

    def get_arg_val(self, key) -> str | None:
        try:
            if key == OptionKey.SESSIONID_SS:
                return self.config[OptionKey.SESSIONID_SS.value]
            if key == OptionKey.TT_TARGET_IDC:
                return self.config[OptionKey.TT_TARGET_IDC.value]
            if key == OptionKey.PROXY:
                return self.args[OptionKey.PROXY.value] or self.config[OptionKey.PROXY.value]
            if key == OptionKey.USERNAME:
                try:
                    return self.args[OptionKey.USERNAME.value]
                except AttributeError:
                    raise NoUsernameEnteredError
            if key == OptionKey.QUALITY:
                if self.args[OptionKey.QUALITY.value] is not None:
                    return self.args[OptionKey.QUALITY.value]
                return Quality.ORIGINAL.value
            if key == OptionKey.WAIT_UNTIL_LIVE:
                return self.args[OptionKey.WAIT_UNTIL_LIVE.value]
            if key == OptionKey.TIMEOUT:
                return self.args[OptionKey.TIMEOUT.value]
            raise InvalidArgKeyError(key)
        except KeyError:
            return None

    def save_arg(self, arg: dict):
        self.args.update(arg)

    def set_program_data_dir(self, program_data_dir: str):
        if not os.path.isabs(program_data_dir):
            program_data_dir = os.path.abspath(program_data_dir)

        if not os.path.exists(program_data_dir):
            os.makedirs(program_data_dir, exist_ok=True)

        self.PROGRAM_DATA_DIR = program_data_dir
        self.CONFIG_PATH = os.path.join(self.PROGRAM_DATA_DIR, "config.toml")

        self.config = self._load_config()

    def _load_config(self) -> dict:
        try:
            with open(self.CONFIG_PATH, 'r') as file:
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
