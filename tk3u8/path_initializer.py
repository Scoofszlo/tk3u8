import logging
import os
from typing import Any, Optional
from platformdirs import user_data_path, user_downloads_path
import toml
from tk3u8.cli.console import console
from tk3u8.constants import APP_NAME, DEFAULT_CONFIG
from tk3u8.messages import messages

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class PathInitializer:
    """
    Singleton class to initialize and manage important file and directory
    paths for the application
    """
    _instance = None

    def __new__(cls, *args: Optional[str], **kwargs: Any) -> 'PathInitializer':
        if not cls._instance:
            cls._instance = super(PathInitializer, cls).__new__(cls)
        return cls._instance

    def __init__(
            self,
            program_data_dir: Optional[str] = None,
            config_file_path: Optional[str] = None,
            downloads_dir: Optional[str] = None
    ) -> None:
        # Prevent re-initialization if already initialized
        if not hasattr(self, "_initialized"):
            self._set_dirs(program_data_dir, config_file_path, downloads_dir)
            self._initialized = True

    def _set_dirs(
            self,
            program_data_dir: Optional[str],
            config_file_path: Optional[str],
            download_dir: Optional[str]
    ) -> None:
        # Set up main directory and file paths
        self.PROGRAM_DATA_DIR = self._set_program_data_dir(program_data_dir)
        self.CONFIG_FILE_PATH = self._set_config_file_path(config_file_path)
        self.DOWNLOAD_DIR = self._set_download_dir(download_dir)

    def _set_program_data_dir(self, program_data_dir: Optional[str]) -> str:
        """Sets and/or creates the program data dir accordingly.

        If user specifies a custom path for program data dir, it will be honored.
        Folders, including parent directories will be created if they don't exist.

        If there is no specified custom dir, it will just use the default path
        instead.
        """

        if program_data_dir:
            base_dir_abspath = os.path.abspath(program_data_dir)

            if not os.path.exists(base_dir_abspath):
                os.makedirs(base_dir_abspath, exist_ok=True)

            return base_dir_abspath

        else:
            default_path = os.path.join(user_data_path(), APP_NAME)
            base_dir_abspath = os.path.abspath(default_path)

            if not os.path.exists(base_dir_abspath):
                os.makedirs(base_dir_abspath, exist_ok=True)

            return base_dir_abspath

    def _set_config_file_path(self, config_file_path: Optional[str]) -> str:
        """Sets and/or creates the config file path accordingly.

        If user specified a custom config file location, it will be honored
        as long as it exists. If not, it will raise an error.

        If there is no specified custom config path, it will just
        """

        if config_file_path:
            if os.path.isfile(config_file_path):
                return os.path.abspath(config_file_path)
            else:
                error_msg = messages.config_file_loading_error
                console.print(error_msg)
                logger.error(error_msg)
                exit(1)
        else:
            default_path = os.path.join(self.PROGRAM_DATA_DIR, "tk3u8.conf")

            if not os.path.isfile(default_path):
                with open(default_path, "w") as file:
                    toml.dump(DEFAULT_CONFIG, file)

            return default_path

    def _set_download_dir(self, download_dir: Optional[str]) -> str:
        """Sets and/or creates the download dir accordingly.

        If user specifies a custom path for download dir, it will be honored.
        Folders, including parent directories will be created if they don't exist.

        If there is no specified custom dir, it will just use the default path
        instead.
        """

        if download_dir:
            download_dir_abspath = os.path.abspath(download_dir)

            if not os.path.exists(download_dir_abspath):
                os.makedirs(download_dir_abspath, exist_ok=True)

            return download_dir_abspath
        else:
            default_path = os.path.join(user_downloads_path(), APP_NAME)
            download_dir_abspath = os.path.abspath(default_path)

            if not os.path.exists(download_dir_abspath):
                os.makedirs(download_dir_abspath, exist_ok=True)

            return download_dir_abspath
