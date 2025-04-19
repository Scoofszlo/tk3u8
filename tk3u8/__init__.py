import os
import toml
from tk3u8.constants import CONFIG_FILE_PATH, DEFAULT_CONFIG, PROGRAM_DATA_DIR


def _init_program_data_dir() -> None:
    if not os.path.exists(PROGRAM_DATA_DIR):
        os.mkdir(PROGRAM_DATA_DIR)


def _init_file_config() -> None:
    if not os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as file:
            toml.dump(DEFAULT_CONFIG, file)


_init_program_data_dir()
_init_file_config()
