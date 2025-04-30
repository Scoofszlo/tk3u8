import json
import re
import time
from bs4 import BeautifulSoup
from datetime import datetime
from yt_dlp import YoutubeDL
from tk3u8.constants import OptionKey, Quality, StreamLink
from tk3u8.exceptions import (
    DownloadError,
    InvalidQualityError,
    InvalidUsernameError,
    LinkNotAvailableError,
    QualityNotAvailableError,
    ScriptTagNotFoundError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    UserNotFoundError,
    UserNotLiveError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler
from tk3u8.utils.paths import paths_handler


class Tk3u8:
    def __init__(self, program_data_dir: str | None = None) -> None:
        paths_handler.set_base_dir(program_data_dir)
        self.raw_data: dict = {}
        self.stream_data: dict = {}
        self.username: str | None = None
        self.quality: str | None = None
        self.timeout: int = 10
        self.options_handler = OptionsHandler()
        self.request_handler = RequestHandler(self.options_handler)

    def download(
            self,
            username: str | None = None,
            quality: str | None = None,
            wait_until_live: bool = False,
            timeout: int = 10
    ) -> None:
        self._process_args(username=username, quality=quality, wait_until_live=wait_until_live, timeout=timeout)
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

    def set_proxy(self, proxy: str | None) -> None:
        self.options_handler.save_arg({OptionKey.PROXY.value: proxy})

        new_proxy = self.options_handler.get_arg_val(OptionKey.PROXY)
        assert isinstance(new_proxy, (str, type(None)))

        self.request_handler.update_proxy(new_proxy)

    def _initialize_data(self) -> None:
        if not self.username:
            new_username = self.options_handler.get_arg_val(OptionKey.USERNAME)
            assert isinstance(new_username, str)
            self.username = new_username

        if not self.raw_data:
            self.raw_data = self._get_raw_data()

        if not self.stream_data:
            self.stream_data = self._get_stream_data()

        if not self.quality:
            new_quality = self.options_handler.get_arg_val(OptionKey.QUALITY)
            assert isinstance(new_quality, str)
            self.quality = new_quality

        new_timeout = self.options_handler.get_arg_val(OptionKey.TIMEOUT)
        assert isinstance(new_timeout, int)
        self.timeout = new_timeout

    def _update_data(self) -> None:
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
            raise QualityNotAvailableError()

    def _get_raw_data(self) -> dict:
        if not self._is_username_valid(self.username):
            raise InvalidUsernameError(self.username)

        response = self.request_handler.get_data(self.username)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise ScriptTagNotFoundError()

        script_content = script_tag.text
        return json.loads(script_content)

    def _get_stream_data(self) -> dict:
        if not self._is_user_exists():
            raise UserNotFoundError(self.username)

        try:
            return json.loads(self.raw_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self.username)

    def _start_download(self, stream_link: StreamLink) -> None:
        print(f"Starting download:\nUsername: @{self.username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.username}-{timestamp}-{stream_link.quality.value.lower()}"
        filename_with_download_dir = paths_handler.DOWNLOAD_DIR + f"/{self.username}/{filename}.%(ext)s"

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

    def _checking_timeout(self) -> None:
        seconds_left = self.timeout
        extra_space = " " * len(str(seconds_left))  # Ensures the entire line is cleared

        while seconds_left >= 0:
            print(f"Retrying in {seconds_left}{extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * 20}", end="\r")

    def _process_args(self, **kwargs) -> None:
        args_dict = {}

        for key, value in kwargs.items():
            for args in list(OptionKey):
                if key in args.value:
                    args_dict.update({key: value})

        self.options_handler.save_arg(args_dict)
