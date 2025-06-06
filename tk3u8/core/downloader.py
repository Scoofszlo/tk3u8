from datetime import datetime
import logging
import os
import time
from yt_dlp import YoutubeDL
from tk3u8.constants import LiveStatus, OptionKey, StreamLink
from tk3u8.cli.console import console, Live, render_lines
from tk3u8.exceptions import DownloadError, UserNotLiveError, UserPreparingForLiveError
from tk3u8.options_handler import OptionsHandler
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.path_initializer import PathInitializer


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(
            self,
            stream_metadata_handler: StreamMetadataHandler,
            options_handler: OptionsHandler
    ) -> None:
        self._path_initializer = PathInitializer()
        self._options_handler = options_handler
        self._stream_metadata_handler = stream_metadata_handler

    def download(self, quality: str):
        username = self._stream_metadata_handler.get_username()
        wait_until_live = self._options_handler.get_option_val(OptionKey.WAIT_UNTIL_LIVE)
        live_status = self._stream_metadata_handler.get_live_status()

        assert isinstance(username, str)
        assert isinstance(wait_until_live, int)
        assert isinstance(live_status, LiveStatus)

        if live_status in (LiveStatus.OFFLINE, LiveStatus.PREPARING_TO_GO_LIVE):
            if not wait_until_live:
                if live_status == LiveStatus.OFFLINE:
                    raise UserNotLiveError(username)
                elif live_status == LiveStatus.PREPARING_TO_GO_LIVE:
                    raise UserPreparingForLiveError(username)

            offline_msg = f"User [b]@{username}[/b] is [red]currently offline[/red]. Awaiting [b]@{username}[/b] to start streaming..."
            self._wait_until_live(offline_msg, live_status)

        console.print(f"User [b]@{username}[/b] is now [b][green]streaming live.[/b][/green]")

        stream_link = self._stream_metadata_handler.get_stream_link(quality)
        self._start_download(username, stream_link)

    def _start_download(self, username: str, stream_link: StreamLink) -> None:
        starting_download_msg = f"Starting download for user [b]@{username}[/b] [grey50](quality: {stream_link.quality}, stream Link: {stream_link.link})[/grey50]"
        console.print(starting_download_msg, end="\n\n")
        logger.debug(starting_download_msg)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}-{timestamp}-{stream_link.quality}"
        filename_with_download_dir = os.path.join(self._path_initializer.DOWNLOAD_DIR, f"{username}", f"{filename}.%(ext)s")

        ydl_opts = {
            'outtmpl': filename_with_download_dir,
            'quiet': False,  # Set to True to suppress output if needed
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
                ydl.download([stream_link.link])

                finished_downloading_msg = f"[green]Finished downloading[/green] [b]{filename}.mp4[/b] [grey50](saved at: {filename_with_download_dir.replace('%(ext)s', 'mp4')})[/grey50]"
                console.print("\n" + finished_downloading_msg)
                logger.debug(finished_downloading_msg)
        except Exception as e:
            logger.exception(f"{DownloadError.__name__}: {DownloadError(e)}")
            raise DownloadError(e)

    def _wait_until_live(self, offline_msg: str, live_status: LiveStatus):
        with Live(render_lines(offline_msg)) as live:
            try:
                while not live_status == LiveStatus.LIVE:
                    self._checking_timeout(live, offline_msg)
                    self._update_data()
                    live_status = self._stream_metadata_handler.get_live_status()
                live.update(render_lines())
            except KeyboardInterrupt:
                live.update(render_lines(offline_msg, "Checking cancelled by user. Exiting..."))
                exit(0)

    def _update_data(self) -> None:
        self._stream_metadata_handler.update_data()

    def _checking_timeout(self, live: Live, offline_msg: str) -> None:
        seconds_left = self._options_handler.get_option_val(OptionKey.TIMEOUT)
        assert isinstance(seconds_left, int)

        seconds_left_len = len(str(seconds_left))
        seconds_extra_space = " " * seconds_left_len

        for remaining in range(seconds_left, -1, -1):
            live.update(render_lines(offline_msg, f"[bold yellow]Retrying in {remaining} seconds{seconds_extra_space}"))
            time.sleep(1)

        live.update(render_lines(offline_msg, "Checking..."))
