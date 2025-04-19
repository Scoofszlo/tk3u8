import toml
from tk3u8.constants import CONFIG_FILE_PATH, ConfigKey
from tk3u8.custom_exceptions import FileParsingError


class Config:
    _instance = None

    def __new__(cls) -> 'Config':
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.config = self._load_config()

    def get_config(self, key) -> str | None:
        if key == ConfigKey.SESSIONID_SS:
            return self.config["sessionid_ss"]
        if key == ConfigKey.TT_TARGET_IDC:
            return self.config["tt-target-idc"]
        if key == ConfigKey.PROXY:
            return self.config["proxy"]
        else:
            raise KeyError

    def _load_config(self) -> dict:
        try:
            with open(CONFIG_FILE_PATH, 'r') as file:
                config = self._fixup_config(toml.load(file))
                return config
        except FileNotFoundError:
            raise FileParsingError()

    def _fixup_config(self, config: dict) -> dict:
        """Turns empty strings into None values"""

        raw_config: dict = config['config']

        for key, value in raw_config.items():
            if value == "":
                raw_config[key] = None

        return raw_config
