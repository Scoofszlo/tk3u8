from argparse import Namespace
import json
import re
from typing import Dict
from bs4 import BeautifulSoup
from yt_dlp import YoutubeDL
from tk3u8.config import Config
from tk3u8.constants import DOWNLOAD_DIR, Quality, StreamLink
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
from tk3u8.request_handler import RequestHandler
from datetime import datetime


class Tk3u8:
    def __init__(self, args):
        self.args: Namespace = args
        self.config: Config = Config()
        self.request_handler = RequestHandler(self.args, self.config)
        self.raw_data = self._get_raw_data()
        self.stream_data = self._get_stream_data()

    def run(self):
        stream_link = self._get_stream_link_by_quality()

        if self._is_user_live():
            self._start_download(stream_link)
        else:
            raise UserNotLiveError(self.args.username)

    def _get_stream_link_by_quality(self) -> StreamLink:
        try:
            if self.args.quality == Quality.ORIGINAL.value.lower():
                return StreamLink(Quality.ORIGINAL, self.stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
            else:
                for quality in list(Quality)[1:]:  # Turns them into a list of its members and skips the first one since it is already checked from the if statement
                    if quality.value.lower() == self.args.quality:
                        return StreamLink(quality, self.stream_data.get("data", None).get(self.args.quality, None).get("main", None).get("hls", None))

            raise InvalidQualityError()
        except AttributeError:
            raise QualityNotAvailableError()

    def _get_raw_data(self) -> Dict:
        if not self._is_username_valid(self.args.username):
            raise InvalidUsernameError(self.args.username)

        response = self.request_handler.get_data(self.args.username)

        soup = BeautifulSoup(response.text, "html.parser")
        script_tag = soup.find("script", {"id": "SIGI_STATE"})

        if not script_tag:
            raise ScriptTagNotFoundError()

        script_content = script_tag.text
        return json.loads(script_content)

    def _get_stream_data(self) -> Dict:
        if not self._is_user_exists():
            raise UserNotFoundError(self.args.username)

        try:
            return json.loads(self.raw_data["LiveRoom"]["liveRoomUserInfo"]["liveRoom"]["streamData"]["pull_data"]["stream_data"])
        except KeyError:
            raise StreamDataNotFoundError(self.args.username)

    def _start_download(self, stream_link: StreamLink):
        print(f"Starting download:\nUsername: @{self.args.username}\nQuality: {stream_link.quality}\nStream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{self.args.username}-{timestamp}-{stream_link.quality.value.lower()}"
        filename_with_download_dir = DOWNLOAD_DIR + f"/{self.args.username}/{filename}.%(ext)s"

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
