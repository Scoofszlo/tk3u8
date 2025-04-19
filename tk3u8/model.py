from argparse import Namespace
import json
import subprocess
from typing import Dict, List
from bs4 import BeautifulSoup
from tk3u8.config import Config
from tk3u8.constants import DOWNLOAD_DIR, Quality, StreamLink
from tk3u8.custom_exceptions import InvalidQualityError, LinkNotAvailableError, ScriptTagNotFoundError, StreamDataNotFoundError, UnknownStatusCodeError, UserNotLiveError, UserNotFoundError
from tk3u8.request_handler import RequestHandler
from datetime import datetime


class Tk3u8:
    def __init__(self, args):
        self.args: Namespace = args
        self.config: Config = Config()
        self.request_handler = RequestHandler(self.args, self.config)
        self.raw_data = self._get_raw_data()
        self.stream_data = self._get_stream_data()
        self.links: List[StreamLink] = []

    def run(self):
        stream_link = self._get_stream_link_by_quality()

        if self._is_user_live():
            self._start_download(stream_link)
        else:
            raise UserNotLiveError(self.args.username)

    def _get_stream_link_by_quality(self) -> StreamLink:
        if self.args.quality == "original":
            return StreamLink(Quality.ORIGINAL, self.stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
        elif self.args.quality == "uhd":
            return StreamLink(Quality.UHD, self.stream_data.get("data", None).get("uhd", None).get("main", None).get("hls", None))
        elif self.args.quality == "hd":
            return StreamLink(Quality.HD, self.stream_data.get("data", None).get("hd", None).get("main", None).get("hls", None))
        elif self.args.quality == "ld":
            return StreamLink(Quality.LD, self.stream_data.get("data", None).get("ld", None).get("main", None).get("hls", None))
        elif self.args.quality == "sd":
            return StreamLink(Quality.SD, self.stream_data.get("data", None).get("sd", None).get("main", None).get("hls", None))
        else:
            raise InvalidQualityError()

    def _get_raw_data(self) -> Dict:
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
        print(f"Starting download:\nUsername: @{self.args.username}\nQuality: {stream_link.quality}\Stream Link: {stream_link.link}\n")

        if not stream_link.link:
            raise LinkNotAvailableError()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = DOWNLOAD_DIR + f"/{self.args.username}/{self.args.username}-{timestamp}-{stream_link.quality.value.lower()}.%(ext)s"

        command = [
            "yt-dlp",
            "-o", filename,
            stream_link.link
        ]

        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Download failed with error: {e}")
        except FileNotFoundError:
            raise FileNotFoundError("yt-dlp is not installed or not found in PATH.")

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
