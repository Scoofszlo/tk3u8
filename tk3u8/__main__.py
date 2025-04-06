from tk3u8.args_handler import ArgsHandler
from tk3u8.model import Tk3u8


if __name__ == "__main__":
    ah = ArgsHandler()
    args = ah.parse_args()

    obj = Tk3u8(args)
    obj.run()
