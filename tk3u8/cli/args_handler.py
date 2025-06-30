import argparse
from rich_argparse import RichHelpFormatter
from tk3u8.cli.utils import display_version
from tk3u8.constants import Quality


class ArgsHandler():
    _instance = None

    def __new__(cls) -> 'ArgsHandler':
        if cls._instance is None:
            cls._instance = super(ArgsHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="tk3u8 - A TikTok live downloader",
            formatter_class=RichHelpFormatter
        )
        self._init_args()

    def parse_args(self) -> argparse.Namespace:
        args = self._parser.parse_args()
        return args

    def _init_args(self) -> None:
        self._parser.add_argument(
            "username",
            help="The username to be used for recording live stream",
        )
        self._parser.add_argument(
            "-q",
            choices=[quality.value for quality in Quality],
            default=Quality.ORIGINAL.value,
            dest="quality",
            help="Specify the quality of the video to download. Default: original"
        )
        self._parser.add_argument(
            "--proxy",
            help="The proxy server to use for downloading. Sample format: 127.0.0.1:8080"
        )
        self._parser.add_argument(
            "--wait-until-live",
            action="store_true",
            help="Let the program wait until the user goes live to start downloading stream",
            default=None
        )
        self._parser.add_argument(
            "--timeout",
            help="Set the timeout in seconds before rechecking if the user is live.",
            type=int,
        )
        self._parser.add_argument(
            "--force-redownload",
            action="store_true",
            help="Forces the program to redownload again while user is still live.",
            default=None
        )
        self._parser.add_argument(
            "--use-h265",
            action="store_true",
            help="Use the H.265 (HEVC) encoded live stream instead of H.264 (AVC)",
            default=None
        )
        self._parser.add_argument(
            "--config-file",
            help="The path of the config file to use",
            default=None
        )
        self._parser.add_argument(
            "--log-level",
            help="Set the logging level (default: no logging if not used)",
            choices=["DEBUG", "ERROR"],
            dest="log_level"
        )
        self._parser.add_argument(
            "-v", "--version",
            help="Show the program's version",
            action="version",
            version=display_version()
        )
