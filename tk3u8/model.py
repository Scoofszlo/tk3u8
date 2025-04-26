from argparse import Namespace
from datetime import datetime
import json
import re
import time
from typing import Dict
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from tk3u8.constants import DOWNLOAD_DIR, OptionKey, Quality, StreamLink
from tk3u8.exceptions import (
    DownloadError,
    InvalidQualityError,
    InvalidUsernameError,
    LinkNotAvailableError,
    QualityNotAvailableError,
    ScriptTagNotFoundError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    UserNotLiveError,
    UserNotFoundError,
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler


class Tk3u8:
    def __init__(self, args: Namespace | None = None):
        self.options_handler = OptionsHandler(args)
        self.request_handler = RequestHandler(self.options_handler)
        self.raw_data: dict | None = None
        self.stream_data: dict | None = None
        self.username: str | None = None
        self.quality: str | None = None
        self.timeout: int | None = None

    def download(
            self,
            username: str | None = None,
            quality: Quality | None = None,
            wait_until_live: bool = False,
            timeout: int = 10
    ):
        script_args = [
            {OptionKey.USERNAME.value: username},
            {OptionKey.QUALITY.value: quality.value if quality else None},
            {OptionKey.WAIT_UNTIL_LIVE.value: wait_until_live},
            {OptionKey.TIMEOUT.value: timeout}
        ]
        [self.options_handler.save_script_args(arg) for arg in script_args]
        self._initialize_data()

        stream_link = self._get_stream_link_by_quality()

        if self._is_user_live():
            self._start_download(stream_link)
            return
        else:
            if not wait_until_live:
                raise UserNotLiveError(self.username)

            print(f"User @{username} is currently offline. Awaiting @{self.username} to start streaming.")
            while not self._is_user_live():
                self._checking_timeout()
                self._update_data()
            print(f"\nUser @{self.username} is now streaming live.")
            self._start_download(stream_link)

    def set_proxy(self, proxy: str):
        self.options_handler.save_script_args({OptionKey.PROXY.value: proxy})
        self.request_handler.update_proxy(proxy)

    def set_program_data_dir(self, program_data_dir):
        self.options_handler.set_program_data_dir(program_data_dir)

    def _initialize_data(self):
        if not self.username:
            self.username = self.options_handler.get_option_val(OptionKey.USERNAME)

        if not self.raw_data:
            self.raw_data = self._get_raw_data()

        if not self.stream_data:
            self.stream_data = self._get_stream_data()

        if not self.quality:
            self.quality = self.options_handler.get_option_val(OptionKey.QUALITY)

        if not self.timeout:
            self.timeout = self.options_handler.get_option_val(OptionKey.TIMEOUT)

    def _update_data(self):
        self.raw_data = self._get_raw_data()
        self.stream_data = self._get_stream_data()

    def _get_stream_link_by_quality(self) -> StreamLink:
        try:
            if self.quality == Quality.ORIGINAL.value.lower():
                return StreamLink(Quality.ORIGINAL, self.stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
            else:
                for quality in list(Quality)[1:]:  # Turns them into a list of its members and skips the first one since it is already checked from the if statement
                    if quality.value.lower() == self.quality:
                        return StreamLink(quality, self.stream_data.get("data", None).get(self.quality, None).get("main", None).get("hls", None))

            raise InvalidQualityError()
        except AttributeError:
            print
            raise QualityNotAvailableError()

    def _get_raw_data(self) -> Dict:
        if not self._is_username_valid(self.username):
            raise InvalidUsernameError(self.username)

        response = self.request_handler.get_data(self.username)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise ScriptTagNotFoundError()

        script_content = script_tag.text
        return json.loads(script_content)

    def _get_stream_data(self) -> Dict:
        if not self._is_user_exists():
            raise UserNotFoundError(self.username)

        try:
            return json.loads(self.raw_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self.username)

    def _start_download(self, stream_link: StreamLink):
        print(f"Starting download:\nUsername: @{self.username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.username}-{timestamp}-{stream_link.quality.value.lower()}"
        filename_with_download_dir = DOWNLOAD_DIR + f"/{self.username}/{filename}.%(ext)s"

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

    def _is_user_live(self) -> bool:
        status = self.raw_data["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]

        if status == 2:
            return True
        elif status == 4:
            return False
        else:
            raise UnknownStatusCodeError(status)

    def _is_user_exists(self) -> bool:
        if self.raw_data.get("LiveRoom"):
            return True
        return False

    def _is_username_valid(self, username) -> bool:
        pattern = r"^[a-z0-9_.]{1,24}$"
        match = re.match(pattern, username)

        if match:
            return True
        return False

    def _checking_timeout(self):
        seconds_left = self.timeout
        extra_space = " " * len(str(seconds_left))  # Ensures the entire line is cleared

        while seconds_left >= 0:
            print(f"\Retrying in {seconds_left}{extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * 20}", end="\r")
