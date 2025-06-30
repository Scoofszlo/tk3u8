import logging
from typing import Optional
import toml
from toml import TomlDecodeError
from tk3u8.cli.console import console
from tk3u8.constants import OptionKey
from tk3u8.messages import messages
from tk3u8.paths_handler import PathsHandler


OPTION_KEY_DEFAULT_VALUES = {
    OptionKey.SESSIONID_SS: None,
    OptionKey.TT_TARGET_IDC: None,
    OptionKey.PROXY: None,
    OptionKey.WAIT_UNTIL_LIVE: False,
    OptionKey.TIMEOUT: 30,
    OptionKey.FORCE_REDOWNLOAD: False,
    OptionKey.USE_H265: False
}

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class OptionsHandler:
    """
    Responsible for managing application options from multiple sources,
    including command-line arguments and configuration files. It provides
    methods to retrieve option values with a defined precedence
    (command-line arguments > config file > defaults), save argument
    values, and validate configuration files.

    Attributes:
        _paths_initializer (PathsHandler): Helper for resolving
            configuration file paths.
        _args_values (dict): Stores option values provided from the
            command-line arguments.
        _config_values (dict): Stores option values loaded from the configuration file.
    """

    def __init__(self, paths_handler: PathsHandler) -> None:
        self._paths_handler = paths_handler
        self._args_values: dict = {}
        self._config_values: dict = self._load_config_values()

    def get_option_val(self, key: OptionKey) -> Optional[str | int | bool]:
        """
        Retrieves the value for a given option key, checking arguments first, then config file,
        and finally falling back to default values.
        """
        val = self._args_values.get(key.value)
        if val is not None:
            return val

        val = self._config_values.get(key.value)
        if val is not None:
            return val

        return OPTION_KEY_DEFAULT_VALUES.get(key)

    def save_args_values(self, *args: dict, **kwargs: Optional[str | int]) -> None:
        """
        Saves provided argument values into the 'self._args_values',
        accepting both dictionaries and keyword arguments.
        """

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
            with open(self._paths_handler.CONFIG_FILE_PATH, 'r') as file:
                config = self._validate_and_retouch_config(toml.load(file))
                return config
        except (FileNotFoundError, UnicodeDecodeError):
            console.print(messages.config_file_parsing_error)
            logger.error(messages.config_file_parsing_error)
            exit(1)

        except TomlDecodeError as e:
            exc_msg = f'{e.msg} (line {e.lineno} column {e.colno} char {e.pos})'
            formatted_msg = messages.config_file_decoding_error.format(exc_msg=exc_msg)

            console.print(formatted_msg)
            logger.debug(formatted_msg)

            exit(1)

    def _validate_and_retouch_config(self, config: dict) -> dict:
        """Validates the configuration dictionary, ensuring all keys are valid
        option keys andconverting empty string values to None."""

        raw_config: dict = config['config']
        option_keys = [option_key.value for option_key in OptionKey]

        for key, value in raw_config.items():
            if key not in option_keys:
                msg = messages.invalid_option_key.format(key=key)
                console.print(msg)
                logger.debug(msg)

                exit(1)

            if value == "":
                raw_config[key] = None

        return raw_config
