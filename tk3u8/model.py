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
    NoUsernameEnteredError,
    QualityNotAvailableError,
    ScriptTagNotFoundError,
    StreamDataNotFoundError,
    UnknownStatusCodeError,
    UserNotFoundError,
    UserNotLiveError
)
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler
from tk3u8.utils.paths import PathsHandler


class Tk3u8:
    def __init__(self, program_data_dir: str | None = None) -> None:
        self._paths_handler = PathsHandler()
        self._paths_handler.set_base_dir(program_data_dir)
        self._raw_data: dict = {}
        self._stream_data: dict = {}
        self._username: str | None = None
        self._quality: str | None = None
        self._timeout: int = 10
        self._options_handler = OptionsHandler()
        self._request_handler = RequestHandler(self._options_handler)

    def download(
            self,
            username: str | None = None,
            quality: str | None = None,
            wait_until_live: bool = False,
            timeout: int = 10
    ) -> None:
        self._options_handler.save_args(username=username, quality=quality, wait_until_live=wait_until_live, timeout=timeout)
        self._initialize_data()

        stream_link = self._get_stream_link_by_quality()

        if self._is_user_live():
            self._start_download(stream_link)
            return
        else:
            if not wait_until_live:
                raise UserNotLiveError(self._username)

            print(f"User @{username} is currently offline. Awaiting @{self._username} to start streaming.")
            while not self._is_user_live():
                self._checking_timeout()
                self._update_data()
            print(f"\nUser @{self._username} is now streaming live.")
            self._start_download(stream_link)

    def set_proxy(self, proxy: str | None) -> None:
        self._options_handler.save_args({OptionKey.PROXY.value: proxy})

        new_proxy = self._options_handler.get_arg_val(OptionKey.PROXY)
        assert isinstance(new_proxy, (str, type(None)))

        self._request_handler.update_proxy(new_proxy)

    def _initialize_data(self) -> None:
        if not self._username:
            new_username = self._options_handler.get_arg_val(OptionKey.USERNAME)
            assert isinstance(new_username, (str, type(None)))

            if not new_username:
                raise NoUsernameEnteredError()

            self._username = new_username

            if not self._is_username_valid(self._username):
                raise InvalidUsernameError(self._username)

        if not self._raw_data:
            self._raw_data = self._get_raw_data()

        if not self._is_user_exists():
            raise UserNotFoundError(self._username)

        if not self._stream_data:
            self._stream_data = self._get_stream_data()

        if not self._quality:
            new_quality = self._options_handler.get_arg_val(OptionKey.QUALITY)
            assert isinstance(new_quality, str)
            self._quality = new_quality

        new_timeout = self._options_handler.get_arg_val(OptionKey.TIMEOUT)
        assert isinstance(new_timeout, int)
        self._timeout = new_timeout

    def _get_raw_data(self) -> dict:
        response = self._request_handler.get_data(self._username)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise ScriptTagNotFoundError()

        script_content = script_tag.text
        return json.loads(script_content)

    def _get_stream_data(self) -> dict:
        try:
            return json.loads(self._raw_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self._username)

    def _get_stream_link_by_quality(self) -> StreamLink:
        try:
            if self._quality == Quality.ORIGINAL.value.lower():
                return StreamLink(Quality.ORIGINAL, self._stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
            else:
                for quality in list(Quality)[1:]:  # Turns them into a list of its members and skips the first one since it is already checked from the if statement
                    if quality.value.lower() == self._quality:
                        return StreamLink(quality, self._stream_data.get("data", None).get(self._quality, None).get("main", None).get("hls", None))

            raise InvalidQualityError()
        except AttributeError:
            raise QualityNotAvailableError()

    def _start_download(self, stream_link: StreamLink) -> None:
        print(f"Starting download:\nUsername: @{self._username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self._username}-{timestamp}-{stream_link.quality.value.lower()}"
        filename_with_download_dir = self._paths_handler.DOWNLOAD_DIR + f"/{self._username}/{filename}.%(ext)s"

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
        self._raw_data = self._get_raw_data()
        self._stream_data = self._get_stream_data()

    def _is_username_valid(self, username) -> bool:
        pattern = r"^[a-z0-9_.]{2,24}$"
        match = re.match(pattern, username)

        if match:
            return True
        return False

    def _is_user_exists(self) -> bool:
        if self._raw_data.get("LiveRoom"):
            return True
        return False

    def _is_user_live(self) -> bool:
        status = self._raw_data["LiveRoom"]["liveRoomUserInfo"]["user"]["status"]

        if status == 2:
            return True
        elif status == 4:
            return False
        else:
            raise UnknownStatusCodeError(status)

    def _checking_timeout(self) -> None:
        seconds_left = self._timeout
        extra_space = " " * len(str(seconds_left))  # Ensures the entire line is cleared

        while seconds_left >= 0:
            print(f"Retrying in {seconds_left}{extra_space}", end="\r")
            seconds_left -= 1
            time.sleep(1)
        print(f"Checking... {' ' * 20}", end="\r")
