from datetime import datetime
import logging
import os
import time
from yt_dlp import YoutubeDL
from tk3u8.constants import LiveStatus, OptionKey, StreamLink
from tk3u8.cli.console import console, Live, render_lines
from tk3u8.exceptions import DownloadError, QualityNotAvailableError
from tk3u8.messages import messages
from tk3u8.options_handler import OptionsHandler
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.paths_handler import PathsHandler


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(
            self,
            paths_handler: PathsHandler,
            stream_metadata_handler: StreamMetadataHandler,
            options_handler: OptionsHandler
    ) -> None:
        self._paths_handler = paths_handler
        self._options_handler = options_handler
        self._stream_metadata_handler = stream_metadata_handler

    def download(self, quality: str) -> None:
        username = self._stream_metadata_handler.get_username()
        wait_until_live = self._options_handler.get_option_val(OptionKey.WAIT_UNTIL_LIVE)
        live_status = self._stream_metadata_handler.get_live_status()
        force_redownload = self._options_handler.get_option_val(OptionKey.FORCE_REDOWNLOAD)
        redownload_attempted = False
        use_h265 = self._options_handler.get_option_val(OptionKey.USE_H265)

        assert isinstance(username, str)
        assert isinstance(wait_until_live, int)
        assert isinstance(live_status, LiveStatus)
        assert isinstance(force_redownload, bool)
        assert isinstance(use_h265, bool)

        while True:
            if live_status in (LiveStatus.OFFLINE, LiveStatus.PREPARING_TO_GO_LIVE):
                # If the user did not use the 'wait until live' option from
                # either the config file or command-line argument, the program
                # will exit momentarily
                if not wait_until_live:
                    if live_status == LiveStatus.OFFLINE:
                        console.print(messages.user_offline.format(username=username))
                        exit(0)
                    elif live_status == LiveStatus.PREPARING_TO_GO_LIVE:
                        console.print(messages.preparing_to_go_live.format(username=username))
                        exit(0)

                # Otherwise, the program will attempt to check the live
                # status every n seconds until the user goes live.
                offline_msg = messages.awaiting_to_go_live.format(username=username)
                self._wait_until_live(offline_msg, live_status)

            if not redownload_attempted:
                console.print(messages.user_is_now_live.format(username=username))
            else:
                console.print(messages.reattempting_download.format(username=username))

            stream_link = self._stream_metadata_handler.get_stream_link(quality, use_h265)
            if not self._is_stream_link_available(stream_link):
                console.print(messages.quality_not_available.format(quality=quality))
                logger.error(f"{QualityNotAvailableError.__name__}: {QualityNotAvailableError()}")
                exit(0)

            self._start_download(username, stream_link)

            if not force_redownload:
                break

            self._show_redownloading_notice()

            self._update_data()
            live_status = live_status = self._stream_metadata_handler.get_live_status()
            redownload_attempted = True

    def _start_download(self, username: str, stream_link: StreamLink) -> None:
        starting_download_msg = messages.starting_download.format(
            username=username,
            stream_link=stream_link
        )
        console.print(starting_download_msg, end="\n\n")
        logger.debug(starting_download_msg)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{username}-{timestamp}-{stream_link.quality}"
        filename_with_download_dir = os.path.join(self._paths_handler.DOWNLOAD_DIR, f"{username}", f"{filename}.%(ext)s")

        ydl_opts = {
            'outtmpl': filename_with_download_dir,
            'quiet': False,  # Set to True to suppress output if needed
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:  # type: ignore[arg-type]
                ydl.download([stream_link.link])

                finished_downloading_msg = messages.finished_downloading.format(
                    filename=filename,
                    filename_with_download_dir=filename_with_download_dir.replace('%(ext)s', 'mp4'),
                )
                console.print("\n" + finished_downloading_msg)
                logger.debug(finished_downloading_msg)
        except Exception as e:
            logger.exception(f"{DownloadError.__name__}: {DownloadError(e)}")
            raise DownloadError(e)

    def _is_stream_link_available(self, stream_link: StreamLink) -> bool:
        if stream_link.link is None:
            return False
        return True

    def _wait_until_live(self, offline_msg: str, live_status: LiveStatus) -> None:
        """
        Waits until the stream becomes live, periodically checking the live
        status. This method displays a live-updating message while the stream
        is offline, repeatedly checking the stream's status until it becomes
        live.
        """

        with Live(render_lines(offline_msg)) as live:
            try:
                while not live_status == LiveStatus.LIVE:
                    self._pause_rechecking(live, offline_msg)
                    self._update_data()
                    live_status = self._stream_metadata_handler.get_live_status()
                live.update(render_lines())
            except KeyboardInterrupt:
                live.update(render_lines(offline_msg, messages.cancelled_checking_live))
                exit(0)

    def _update_data(self) -> None:
        self._stream_metadata_handler.update_data()

    def _pause_rechecking(self, live: Live, offline_msg: str) -> None:
        """
        Handles temporarily pausing before rechecking live status,
        and prints the seconds remaining before the next check.
        """

        seconds_left = self._options_handler.get_option_val(OptionKey.TIMEOUT)
        assert isinstance(seconds_left, int)

        seconds_left_len = len(str(seconds_left))
        seconds_extra_space = " " * seconds_left_len

        for remaining in range(seconds_left, -1, -1):
            live.update(render_lines(offline_msg, messages.retrying_to_check_live.format(
                remaining=remaining,
                seconds_extra_space=seconds_extra_space
            )))
            time.sleep(1)

        live.update(render_lines(offline_msg, messages.ongoing_checking_live))

    def _show_redownloading_notice(self) -> None:
        """
        Displays a message notifying the user that they have 5 seconds to
        exit the program to avoid redownloading the stream.

        This only occurs if the user uses the 'FORCE_REDOWNLOAD' option from
        the config file or command-line argument.
        """

        with Live() as live:
            try:
                for remaining_seconds in range(5, -1, -1):
                    live.update(render_lines("\n" + messages.redownloading_notice.format(remaining=remaining_seconds)))
                    time.sleep(1)
            except KeyboardInterrupt:
                live.update(render_lines(messages.exiting_download_reattempt))
                exit(0)
