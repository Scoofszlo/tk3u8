import logging
from typing import Optional
from tk3u8.cli.console import console
from tk3u8.constants import OptionKey, Quality
from tk3u8.core.downloader import Downloader
from tk3u8.core.stream_metadata_handler import StreamMetadataHandler
from tk3u8.messages import messages
from tk3u8.options_handler import OptionsHandler
from tk3u8.path_initializer import PathInitializer
from tk3u8.session.request_handler import RequestHandler


logger = logging.getLogger(__name__)


class Tk3u8:
    """
    Serves as the main entry point and public API, organizing all core modules
    and functionalities in this single interface, allowing users to easily
    setup their scripts.

    This class is designed to simplify usage by encapsulating the
    initialization and coordination of various internal components,
    such as path handling, options management, HTTP requests, stream
    metadata processing, and downloading logic. Users are encouraged to
    interact with this class directly when integrating tk3u8 into their
    scripts.
    """
    def __init__(
            self,
            program_data_dir: Optional[str] = None,
            config_file_path: Optional[str] = None,
            downloads_dir: Optional[str] = None
    ) -> None:
        logger.debug("Initializing Tk3u8 class")
        self._paths_handler = PathInitializer(program_data_dir, config_file_path, downloads_dir)
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
            wait_until_live: Optional[bool] = None,
            timeout: Optional[int] = None,
            force_redownload: Optional[bool] = None,
            use_h265: Optional[bool] = None
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
            force_redownload=force_redownload,
            use_h265=use_h265
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

    def set_cookies(self, cookies: dict) -> None:
        for key, value in cookies.items():
            if key == OptionKey.SESSIONID_SS.value:
                self._options_handler.save_args_values({OptionKey.SESSIONID_SS.value: value})
            elif key == OptionKey.TT_TARGET_IDC.value:
                self._options_handler.save_args_values({OptionKey.TT_TARGET_IDC.value: value})
            else:
                error_msg = messages.invalid_cookie_key_error.format(key=key)
                console.print(error_msg)
                logger.error(error_msg)
                exit(1)

        new_sessionid_ss = self._options_handler.get_option_val(OptionKey.SESSIONID_SS)
        new_tt_target_idc = self._options_handler.get_option_val(OptionKey.TT_TARGET_IDC)

        assert isinstance(new_sessionid_ss, str)
        assert isinstance(new_tt_target_idc, str)

        self._request_handler.update_cookies(new_sessionid_ss, new_tt_target_idc)
