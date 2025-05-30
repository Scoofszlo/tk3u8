import os
import toml
from tk3u8.constants import DEFAULT_CONFIG


class PathInitializer:
    """
    Singleton class to initialize and manage important file and directory
    paths for the application
    """
    _instance = None

    def __new__(cls, *args, **kwargs) -> 'PathInitializer':
        if not cls._instance:
            cls._instance = super(PathInitializer, cls).__new__(cls)
        return cls._instance

    def __init__(self, base_dir=None):
        # Prevent re-initialization if already initialized
        if not hasattr(self, "_initialized"):
            self._set_base_dir(base_dir)
            self._initialized = True

    def _set_base_dir(self, base_dir) -> None:
        # Set up main directory and file paths
        self.PROGRAM_DATA_DIR = base_dir if base_dir else "user_data"
        self.STREAM_DATA_FILE = os.path.join(self.PROGRAM_DATA_DIR, "stream_data.json")
        self.CONFIG_FILE_PATH = os.path.join(self.PROGRAM_DATA_DIR, "config.toml")
        self.DOWNLOAD_DIR = os.path.join(self.PROGRAM_DATA_DIR, "downloads")

        self._initialize_paths()

    def _initialize_paths(self) -> None:
        if not os.path.isabs(self.PROGRAM_DATA_DIR):
            self.PROGRAM_DATA_DIR = os.path.abspath(self.PROGRAM_DATA_DIR)

        if not os.path.exists(self.PROGRAM_DATA_DIR):
            os.mkdir(self.PROGRAM_DATA_DIR)

        if not os.path.isfile(self.CONFIG_FILE_PATH):
            with open(self.CONFIG_FILE_PATH, "w") as file:
                toml.dump(DEFAULT_CONFIG, file)
