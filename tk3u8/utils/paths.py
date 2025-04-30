import os

import toml

from tk3u8.constants import DEFAULT_CONFIG


class PathsHandler:
    def set_base_dir(self, base_dir):
        self.PROGRAM_DATA_DIR = base_dir if base_dir else "user_data"
        self.STREAM_DATA_FILE = os.path.join(self.PROGRAM_DATA_DIR, "stream_data.json")
        self.CONFIG_FILE_PATH = os.path.join(self.PROGRAM_DATA_DIR, "config.toml")
        self.DOWNLOAD_DIR = os.path.join(self.PROGRAM_DATA_DIR, "downloads")

        self._initialize_paths()

    def _initialize_paths(self):
        if not os.path.isabs(self.PROGRAM_DATA_DIR):
            self.PROGRAM_DATA_DIR = os.path.abspath(self.PROGRAM_DATA_DIR)

        if not os.path.exists(self.PROGRAM_DATA_DIR):
            os.mkdir(self.PROGRAM_DATA_DIR)

        if not os.path.isfile(self.CONFIG_FILE_PATH):
            with open(self.CONFIG_FILE_PATH, "w") as file:
                toml.dump(DEFAULT_CONFIG, file)


paths_handler = PathsHandler()
