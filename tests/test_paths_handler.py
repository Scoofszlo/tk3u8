import os
import shutil
import tempfile
from platformdirs import user_data_path, user_downloads_path
from unittest.mock import patch
from tk3u8.constants import APP_NAME
from tk3u8.paths_handler import PathsHandler


def test_default_paths():
    with patch("os.makedirs"), patch("os.path.exists", return_value=True):
        paths_handler = PathsHandler()
        PROGRAM_DATA_DIR = paths_handler.PROGRAM_DATA_DIR
        CONFIG_FILE_PATH = paths_handler.CONFIG_FILE_PATH
        DOWNLOAD_DIR = paths_handler.DOWNLOAD_DIR

        DEFAULT_PROGRAM_DATA_DIR = os.path.abspath(os.path.join(user_data_path(), APP_NAME))
        DEFAULT_CONFIG_FILE_PATH = os.path.abspath(os.path.join(DEFAULT_PROGRAM_DATA_DIR, "tk3u8.conf"))
        DEFAULT_DOWNLOAD_DIR = os.path.abspath(os.path.join(user_downloads_path(), APP_NAME))

        assert PROGRAM_DATA_DIR == DEFAULT_PROGRAM_DATA_DIR
        assert CONFIG_FILE_PATH == DEFAULT_CONFIG_FILE_PATH
        assert DOWNLOAD_DIR == DEFAULT_DOWNLOAD_DIR


def test_custom_program_data_dir():
    temp_dir = tempfile.mkdtemp()

    try:
        with patch("os.makedirs"), patch("os.path.exists", return_value=True):
            paths_handler = PathsHandler(program_data_dir=temp_dir)
            PROGRAM_DATA_DIR = paths_handler.PROGRAM_DATA_DIR
            CONFIG_FILE_PATH = paths_handler.CONFIG_FILE_PATH
            DOWNLOAD_DIR = paths_handler.DOWNLOAD_DIR

            assert PROGRAM_DATA_DIR == os.path.abspath(temp_dir)

            # Config file should be inside the custom dir
            expected_config_path = os.path.abspath(os.path.join(temp_dir, "tk3u8.conf"))
            assert CONFIG_FILE_PATH == expected_config_path

            # Download dir should still be default
            DEFAULT_DOWNLOAD_DIR = os.path.abspath(os.path.join(user_downloads_path(), APP_NAME))
            assert DOWNLOAD_DIR == DEFAULT_DOWNLOAD_DIR
    finally:
        shutil.rmtree(temp_dir)


def test_custom_config_file_path():
    temp_dir = tempfile.mkdtemp()
    custom_config_path = os.path.join(temp_dir, "myconfig.conf")

    # Create the custom config
    with open(custom_config_path, "w") as f:
        f.write("")

    try:
        with patch("os.makedirs"), patch("os.path.exists", return_value=True):
            paths_handler = PathsHandler(config_file_path=custom_config_path)
            PROGRAM_DATA_DIR = paths_handler.PROGRAM_DATA_DIR
            CONFIG_FILE_PATH = paths_handler.CONFIG_FILE_PATH
            DOWNLOAD_DIR = paths_handler.DOWNLOAD_DIR

            # Program data dir should be default
            DEFAULT_PROGRAM_DATA_DIR = os.path.abspath(os.path.join(user_data_path(), APP_NAME))
            assert PROGRAM_DATA_DIR == DEFAULT_PROGRAM_DATA_DIR

            # Config file should be the custom one
            assert CONFIG_FILE_PATH == os.path.abspath(custom_config_path)

            # Download dir should be default
            DEFAULT_DOWNLOAD_DIR = os.path.abspath(os.path.join(user_downloads_path(), APP_NAME))
            assert DOWNLOAD_DIR == DEFAULT_DOWNLOAD_DIR
    finally:
        shutil.rmtree(temp_dir)


def test_custom_downloads_dir():
    temp_dir = tempfile.mkdtemp()

    try:
        with patch("os.makedirs"), patch("os.path.exists", return_value=True):
            paths_handler = PathsHandler(downloads_dir=temp_dir)
            PROGRAM_DATA_DIR = paths_handler.PROGRAM_DATA_DIR
            CONFIG_FILE_PATH = paths_handler.CONFIG_FILE_PATH
            DOWNLOAD_DIR = paths_handler.DOWNLOAD_DIR

            # Program data dir should be default
            DEFAULT_PROGRAM_DATA_DIR = os.path.abspath(os.path.join(user_data_path(), APP_NAME))
            assert PROGRAM_DATA_DIR == DEFAULT_PROGRAM_DATA_DIR

            # Config file should be default
            DEFAULT_CONFIG_FILE_PATH = os.path.abspath(os.path.join(DEFAULT_PROGRAM_DATA_DIR, "tk3u8.conf"))
            assert CONFIG_FILE_PATH == DEFAULT_CONFIG_FILE_PATH

            # Download dir should be the custom one
            assert DOWNLOAD_DIR == os.path.abspath(temp_dir)
    finally:
        shutil.rmtree(temp_dir)
