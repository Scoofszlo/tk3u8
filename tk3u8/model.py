import json
import re
import time
from typing import Optional, cast
from bs4 import BeautifulSoup
from datetime import datetime
from yt_dlp import YoutubeDL
from tk3u8.constants import OptionKey, Quality, StreamLink
from tk3u8.exceptions import (
    DownloadError,
    InvalidQualityError,
    InvalidUsernameError,
    LinkNotAvailableError,
    NoUsernameEnteredError,
    QualityNotAvailableError,
    SourceDataExtractionError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    UserNotFoundError,
    UserNotLiveError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler
from tk3u8.stream_metadata_handler import StreamMetadataHandler
from tk3u8.utils.paths import PathsHandler


class Tk3u8:
    def __init__(self, program_data_dir: str | None = None) -> None:
        self._paths_handler = PathsHandler()
        self._paths_handler.set_base_dir(program_data_dir)
        self._timeout: int = 10
        self._options_handler = OptionsHandler()
        self._request_handler = RequestHandler(self._options_handler)
        self._stream_metadata_handler = StreamMetadataHandler(
            self._request_handler,
            self._options_handler
        )

    def download(
            self,
            username: str | None = None,
            quality: str | None = None,
            wait_until_live: bool = False,
            timeout: int = 10
    ) -> None:
        self._save_args(username=username, quality=quality, wait_until_live=wait_until_live, timeout=timeout)
        self._initialize_data()

        username = cast(str | None, self._get_arg_val(OptionKey.USERNAME))
        stream_link = self._get_stream_link()

        assert isinstance(username, str)

        if self._is_user_live():
            self._start_download(username, stream_link)
            return
        else:
            if not wait_until_live:
                raise UserNotLiveError(username)

            print(f"User @{username} is currently offline. Awaiting @{username} to start streaming.")
            while not self._is_user_live():
                self._checking_timeout()
                self._update_data()
            print(f"\nUser @{username} is now streaming live.")
            self._start_download(username, stream_link)

    def set_proxy(self, proxy: str | None) -> None:
        self._options_handler.save_args({OptionKey.PROXY.value: proxy})

        new_proxy = self._options_handler.get_arg_val(OptionKey.PROXY)
        assert isinstance(new_proxy, (str, type(None)))

        self._request_handler.update_proxy(new_proxy)

    def _initialize_data(self) -> None:
        new_timeout = self._options_handler.get_arg_val(OptionKey.TIMEOUT)
        assert isinstance(new_timeout, int)
        self._timeout = new_timeout

        self._stream_metadata_handler._initialize_data()

    def _update_data(self) -> None:
        self._stream_metadata_handler._update_data()

    def _get_stream_link(self) -> StreamLink:
        return self._stream_metadata_handler.get_stream_link()

    def _is_user_live(self) -> bool:
        return self._stream_metadata_handler.is_user_live()

    def _start_download(self, username: str, stream_link: StreamLink) -> None:
        print(f"Starting download:\nUsername: @{username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{username}-{timestamp}-{stream_link.quality.value.lower()}"
        filename_with_download_dir = self._paths_handler.DOWNLOAD_DIR + f"/{username}/{filename}.%(ext)s"

        ydl_opts = {
            'outtmpl': filename_with_download_dir,
            'quiet': False,  # Set to True to suppress output if needed
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
                ydl.download([stream_link.link])
                print(f"\nFinished downloading {filename}.mp4")
        except Exception as e:
            raise DownloadError(e)

    def _checking_timeout(self) -> None:
        seconds_left = self._timeout
        extra_space = " " * len(str(seconds_left))  # Ensures the entire line is cleared

        while seconds_left >= 0:
            print(f"Retrying in {seconds_left}{extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * 20}", end="\r")

    def _save_args(self, *args, **kwargs) -> None:
        self._options_handler.save_args(*args, **kwargs)

    def _get_arg_val(self, key) -> Optional[str | int]:
        return self._options_handler.get_arg_val(key)
