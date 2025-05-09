from typing import Optional, cast
from tk3u8.constants import OptionKey, Quality, StreamLink
from tk3u8.core.downloader import Downloader
from tk3u8.options_handler import OptionsHandler
from tk3u8.request_handler import RequestHandler
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.path_initializer import PathInitializer


class Tk3u8:
    def __init__(self, program_data_dir: str | None = None) -> None:
        self._paths_handler = PathInitializer()
        self._paths_handler.set_base_dir(program_data_dir)
        self._options_handler = OptionsHandler()
        self._request_handler = RequestHandler(self._options_handler)
        self._stream_metadata_handler = StreamMetadataHandler(
            self._request_handler,
            self._options_handler
        )
        self._downloader = Downloader(
            self._stream_metadata_handler,
            self._options_handler
        )

    def download(
            self,
            username: str,
            quality: str = Quality.ORIGINAL.value,
            wait_until_live: bool = False,
            timeout: int = 10
    ) -> None:
        self._save_args(username=username, quality=quality, wait_until_live=wait_until_live, timeout=timeout)
        self._initialize_data()

        username = cast(str, self._stream_metadata_handler._username)
        stream_link = self._get_stream_link()

        assert isinstance(username, str)

        self._downloader.download(username=username, stream_link=stream_link, wait_until_live=wait_until_live)

    def set_proxy(self, proxy: str | None) -> None:
        self._options_handler.save_args({OptionKey.PROXY.value: proxy})

        new_proxy = self._options_handler.get_arg_val(OptionKey.PROXY)
        assert isinstance(new_proxy, (str, type(None)))

        self._request_handler.update_proxy(new_proxy)

    def _initialize_data(self) -> None:
        self._stream_metadata_handler._initialize_data()

    def _get_stream_link(self) -> StreamLink:
        return self._stream_metadata_handler.get_stream_link()

    def _save_args(self, *args, **kwargs) -> None:
        self._options_handler.save_args(*args, **kwargs)

    def _get_arg_val(self, key) -> Optional[str | int]:
        return self._options_handler.get_arg_val(key)
