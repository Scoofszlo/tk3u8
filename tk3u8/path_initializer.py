import os
from typing import Any
import toml
from platformdirs import user_data_path, user_downloads_path
from tk3u8.constants import APP_NAME, DEFAULT_CONFIG


class PathInitializer:
    """
    Singleton class to initialize and manage important file and directory
    paths for the application
    """
    _instance = None

    def __new__(cls, *args: dict, **kwargs: Any) -> 'PathInitializer':
        if not cls._instance:
            cls._instance = super(PathInitializer, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_dir: str | None = None):
        # Prevent re-initialization if already initialized
        if not hasattr(self, "_initialized"):
            self._set_base_dir(base_dir)
            self._initialized = True

    def _set_base_dir(self, base_dir: str | None) -> None:
        # Set up main directory and file paths
        self.PROGRAM_DATA_DIR = base_dir if base_dir else self._get_default_base_path()
        self.CONFIG_FILE_PATH = os.path.join(self.PROGRAM_DATA_DIR, "tk3u8.conf")
        self.DOWNLOAD_DIR = os.path.join(user_downloads_path(), APP_NAME)

        self._initialize_paths()

    def _initialize_paths(self) -> None:
        if not os.path.isabs(self.PROGRAM_DATA_DIR):
            self.PROGRAM_DATA_DIR = os.path.abspath(self.PROGRAM_DATA_DIR)

        if not os.path.exists(self.PROGRAM_DATA_DIR):
            os.makedirs(self.PROGRAM_DATA_DIR, exist_ok=True)

        if not os.path.isfile(self.CONFIG_FILE_PATH):
            with open(self.CONFIG_FILE_PATH, "w") as file:
                toml.dump(DEFAULT_CONFIG, file)

    def _get_default_base_path(self) -> str:
        return os.path.join(user_data_path(), APP_NAME)
