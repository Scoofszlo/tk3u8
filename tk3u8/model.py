from argparse import Namespace
import json
import subprocess
from typing import Dict, List
from bs4 import BeautifulSoup

from tk3u8.constants import Mode, Quality, DownloadLink
from tk3u8.custom_exceptions import InvalidQualityError, LinkNotAvailableError, ScriptTagNotFoundError, StreamDataNotFoundError, UnknownStatusCodeError, UserNotLiveError, UserNotFoundError
from tk3u8.request_handler import RequestHandler


class Tk3u8:
    def __init__(self, args):
        self.args: Namespace = args
        self.request_handler = RequestHandler()
        self.identify_mode = self._identify_mode()
        self.raw_data = self._get_raw_data()
        self.stream_data = self._get_stream_data()
        self.links: List[DownloadLink] = []

    def run(self):
        download_link = self._get_download_link_by_quality()

        if self._is_user_live():
            self._start_download(download_link)
        else:
            raise UserNotLiveError(self.args.username)

    def _identify_mode(self):
        if self.args.mode == "auto":
            return Mode.AUTO
        if self.args.mode == "manual":
            return Mode.MANUAL

    def _get_download_link_by_quality(self) -> DownloadLink:
        if self.args.quality == "original":
            return DownloadLink(Quality.ORIGINAL, self.stream_data.get("data", None).get("origin", None).get("main", None).get("hls", None))
        elif self.args.quality == "uhd":
            return DownloadLink(Quality.UHD, self.stream_data.get("data", None).get("uhd", None).get("main", None).get("hls", None))
        elif self.args.quality == "hd":
            return DownloadLink(Quality.HD, self.stream_data.get("data", None).get("hd", None).get("main", None).get("hls", None))
        elif self.args.quality == "ld":
            return DownloadLink(Quality.LD, self.stream_data.get("data", None).get("ld", None).get("main", None).get("hls", None))
        elif self.args.quality == "sd":
            return DownloadLink(Quality.SD, self.stream_data.get("data", None).get("sd", None).get("main", None).get("hls", None))
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

    def _start_download(self, download_link: DownloadLink):
        print(f"Starting download:\nUsername: @{self.args.username}\nQuality: {download_link.quality}\nDownload Link: {download_link.link}\n")

        if not download_link.link:
            raise LinkNotAvailableError()

        command = [
            "yt-dlp",
            download_link.link
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
