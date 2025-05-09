from tk3u8.args_handler import ArgsHandler
from tk3u8.core.api import Tk3u8


if __name__ == "__main__":
    ah = ArgsHandler()
    args = ah.parse_args()

    username = args.username
    quality = args.quality
    proxy = args.proxy

    tk3u8 = Tk3u8()
    tk3u8.set_proxy(proxy)
    tk3u8.download(username=username, quality=quality)
