from tk3u8.cli.args_handler import ArgsHandler
from tk3u8.cli.logging import setup_logging


def start_cli() -> None:
    from tk3u8.core.model import Tk3u8

    ah = ArgsHandler()
    args = ah.parse_args()

    username = args.username
    quality = args.quality
    proxy = args.proxy
    wait_until_live = args.wait_until_live
    timeout = args.timeout
    log_level = args.log_level
    force_redownload = args.force_redownload
    use_h265 = args.use_h265
    config_file_path = args.config_file

    setup_logging(log_level)

    tk3u8 = Tk3u8(config_file_path=config_file_path)
    tk3u8.set_proxy(proxy)
    tk3u8.download(
        username=username,
        quality=quality,
        wait_until_live=wait_until_live,
        timeout=timeout,
        force_redownload=force_redownload,
        use_h265=use_h265
    )
