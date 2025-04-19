import argparse


class ArgsHandler():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ArgsHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.parser: argparse.ArgumentParser = argparse.ArgumentParser(
            description="tk3u8 - A TikTok live downloader"
        )
        self.init_args()

    def parse_args(self) -> argparse.Namespace:
        args = self.parser.parse_args()
        return args

    def init_args(self) -> None:
        self.parser.add_argument("-u", "--username", help="The username to be used for recording live stream", required=True)
        self.parser.add_argument(
            "-q",
            choices=[
                "original",
                "uhd",
                "hd",
                "ld",
                "sd"
            ],
            default="original",
            dest="quality",
            help="Specify the quality of the video to download. Default: original"
        )
