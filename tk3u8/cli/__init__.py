import logging
import os
from datetime import datetime
from tk3u8.cli.args_handler import ArgsHandler
from tk3u8.core.model import Tk3u8
from tk3u8 import logger


def start_cli() -> None:
    ah = ArgsHandler()
    args = ah.parse_args()

    username = args.username
    quality = args.quality
    proxy = args.proxy
    wait_until_live = args.wait_until_live
    timeout = args.timeout

    _setup_logging()

    tk3u8 = Tk3u8()
    tk3u8.set_proxy(proxy)
    tk3u8.download(
        username=username,
        quality=quality,
        wait_until_live=wait_until_live,
        timeout=timeout
    )


def _setup_logging() -> None:
    logger.setLevel(logging.DEBUG)

    log_directory = os.path.join("user_data", "logs")

    if not os.path.exists(log_directory):
        os.mkdir(log_directory)

    log_filename = f"logs-{datetime.now().strftime('%Y%m%d')}.log"
    log_file = os.path.join(log_directory, log_filename)

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(name)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S%z'))
    logger.addHandler(file_handler)


if __name__ == "__main__":
    start_cli()
