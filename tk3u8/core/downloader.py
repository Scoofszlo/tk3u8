from datetime import datetime
import time
from yt_dlp import YoutubeDL
from tk3u8.constants import LiveStatus, OptionKey, StreamLink
from tk3u8.exceptions import DownloadError, UserNotLiveError, UserPreparingForLiveError
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

    def download(self):
        username = self._stream_metadata_handler._username
        wait_until_live = self._options_handler.get_option_val(OptionKey.WAIT_UNTIL_LIVE)
        live_status = self._stream_metadata_handler._live_status

        assert isinstance(username, str)
        assert isinstance(wait_until_live, int)
        assert isinstance(live_status, LiveStatus)

        if live_status in (LiveStatus.OFFLINE, LiveStatus.PREPARING_TO_GO_LIVE):
            if not wait_until_live:
                if live_status == LiveStatus.OFFLINE:
                    raise UserNotLiveError(username)
                elif live_status == LiveStatus.PREPARING_TO_GO_LIVE:
                    raise UserPreparingForLiveError(username)

            print(f"User @{username} is currently offline. Awaiting @{username} to start streaming.")

            try:
                while not live_status == LiveStatus.LIVE:
                    self._checking_timeout()
                    self._update_data()
                    live_status = self._stream_metadata_handler._live_status
                    assert isinstance(live_status, LiveStatus)
            except KeyboardInterrupt:
                print("Checking cancelled by user. Exiting...")
                exit(0)

            print(f"\nUser @{username} is now streaming live.")

        stream_link = self._stream_metadata_handler.get_stream_link()

        self._start_download(username, stream_link)

    def _start_download(self, username: str, stream_link: StreamLink) -> None:
        print(f"Starting download:\nUsername: @{username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

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

        seconds_left_len = len(str(seconds_left))
        seconds_extra_space = " " * seconds_left_len
        checking_extra_space = 8 + seconds_left_len

        while seconds_left >= 0:
            print(f"Retrying in {seconds_left} seconds{seconds_extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * (checking_extra_space)}", end="\r")
