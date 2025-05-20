from datetime import datetime
import time
from yt_dlp import YoutubeDL
from tk3u8.constants import OptionKey, StreamLink
from tk3u8.core import helper as hlp
from tk3u8.exceptions import DownloadError, LinkNotAvailableError, UserNotLiveError
from tk3u8.options_handler import OptionsHandler
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.path_initializer import PathInitializer


class Downloader:
    def __init__(
            self,
            stream_metadata_handler: StreamMetadataHandler,
            options_handler: OptionsHandler
    ) -> None:
        self._path_initializer = PathInitializer()
        self._options_handler = options_handler
        self._stream_metadata_handler = stream_metadata_handler

    def download(self, username: str, stream_link: StreamLink, wait_until_live: bool):
        source_data = self._stream_metadata_handler._source_data

        if hlp.is_user_live(source_data):
            self._start_download(username, stream_link)
        else:
            if not wait_until_live:
                raise UserNotLiveError(username)

            print(f"User @{username} is currently offline. Awaiting @{username} to start streaming.")
            while not hlp.is_user_live(source_data):
                self._checking_timeout()
                self._update_data()
                source_data = self._stream_metadata_handler._source_data
            print(f"\nUser @{username} is now streaming live.")
            self._start_download(username, stream_link)

    def _start_download(self, username: str, stream_link: StreamLink) -> None:
        print(f"Starting download:\nUsername: @{username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{username}-{timestamp}-{stream_link.quality}"
        filename_with_download_dir = self._path_initializer.DOWNLOAD_DIR + f"/{username}/{filename}.%(ext)s"

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

    def _update_data(self) -> None:
        self._stream_metadata_handler.update_data()

    def _checking_timeout(self) -> None:
        seconds_left = self._options_handler.get_option_val(OptionKey.TIMEOUT)
        assert isinstance(seconds_left, int)

        extra_space = " " * len(str(seconds_left))  # Ensures the entire line is cleared

        while seconds_left >= 0:
            print(f"Retrying in {seconds_left}{extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * 20}", end="\r")
