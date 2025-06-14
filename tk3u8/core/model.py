import logging
from tk3u8.constants import OptionKey, Quality
from tk3u8.core.downloader import Downloader
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.options_handler import OptionsHandler
from tk3u8.path_initializer import PathInitializer
from tk3u8.session.request_handler import RequestHandler


logger = logging.getLogger(__name__)


class Tk3u8:
    """
    Serves as the main entry point and public API, organizing all core modules
    and functionalities in this single interface.

    This class is designed to simplify usage by encapsulating the
    initialization and coordination of various internal components,
    such as path handling, options management, HTTP requests, stream
    metadata processing, and downloading logic. Users are encouraged to
    interact with this class directly when integrating tk3u8 into their
    scripts, as it provides a unified and stable interface for all major
    operations.
    """
    def __init__(self, program_data_dir: str | None = None) -> None:
        logger.debug("Initializing Tk3u8 class")
        self._paths_handler = PathInitializer(program_data_dir)
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
            timeout: int = 30,
            force_redownload: bool = False
    ) -> None:
        """
        Downloads a stream for the specified user with the given quality and options.
        Args:
            username (str): The username of the stream to download.
            quality (str, optional): The desired stream quality. Defaults to
                original".
            wait_until_live (bool, optional): Whether to wait until the stream
                is live before downloading. Defaults to False.
            timeout (int, optional): The timeout (in seconds) before rechecking
                if the user is llive. Defaults to 30.
            force_redownload (bool, optional): Force re-download while the user
                is live. Use this if you encounter auto-stopping of download.
                Defaults to False.
        """
        self._options_handler.save_args_values(
            wait_until_live=wait_until_live,
            timeout=timeout,
            force_redownload=force_redownload
        )
        self._stream_metadata_handler.initialize_data(username)
        self._downloader.download(quality)

    def set_proxy(self, proxy: str | None) -> None:
        """
        Sets the proxy configuration.

        Args:
            proxy (str | None): The proxy address to set (e.g., 127.0.0.1:8080).
        """
        self._options_handler.save_args_values({OptionKey.PROXY.value: proxy})

        new_proxy = self._options_handler.get_option_val(OptionKey.PROXY)
        assert isinstance(new_proxy, (str, type(None)))

        self._request_handler.update_proxy(new_proxy)
