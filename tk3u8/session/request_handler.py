import logging
import random
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from tk3u8.constants import USER_AGENT_LIST, OptionKey
from tk3u8.exceptions import RequestFailedError
from tk3u8.options_handler import OptionsHandler


logger = logging.getLogger(__name__)


class RequestHandler:
    """
    Handles HTTP requests with session management, proxy, and cookie support.
    This class manages a requests.Session object, allowing for persistent cookies,
    proxy configuration, and dynamic User-Agent selection. It provides methods to
    fetch data from URLs, update proxy settings, and configure session cookies
    based on provided options.

    Args:
        options_handler (OptionsHandler): An instance responsible for providing
            configuration options such as cookies and proxy settings.

    Attributes:
        _options_handler (OptionsHandler): Stores the options handler instance.
        _session (requests.Session): The session object used for HTTP requests.
        _response (requests.Response): Stores the most recent response object.
    """
    def __init__(self, options_handler: OptionsHandler) -> None:
        self._options_handler = options_handler
        self._session: requests.Session
        self._initialize_session()

    def get_data(self, url: str) -> requests.Response:
        retries = 3
        exc_msg: str = ""

        for retry in range(1, retries + 1):
            try:
                response = self._session.get(url)
                status_code = response.status_code

                if status_code != 200:
                    raw_exc_msg = f"Request error due to status code: {status_code}"
                    exc_msg = f"{RequestFailedError.__name__}: {RequestFailedError(raw_exc_msg)}"

                    if retry == 3:
                        break

                    logger.warning(exc_msg)
                    continue

                return response

            except (ConnectionError, ReadTimeout) as e:
                logger.warning(f"{type(e).__name__} occurred on attempt #{retry}: {e}")

                if retry == 3:
                    exc_msg = f"{RequestFailedError.__name__}: {RequestFailedError(str(e))}"
                    logger.exception(exc_msg)

                    break

                # Re-initalizes the sesssion instance to discard the previous
                # instance as the established connection of it is likely to
                # be staled, so we need to re-initialized this to create new
                # connection.
                self._initialize_session(reinitialized=True)

        raise RequestFailedError(exc_msg)

    def update_proxy(self, proxy: str | None) -> None:
        if proxy:
            self._session.proxies.update({
                    "http": proxy,
                    "https": proxy
            })

            logger.debug(f"Proxy updated to: {proxy}")

    def update_cookies(self, sessionid_ss: str, tt_target_idc: str) -> None:
        self._session.cookies.update({
                "sessionid_ss": sessionid_ss,
                "tt-target-idc": tt_target_idc
            })
        logger.debug(f"'sessionid_ss' cookie updated to: {sessionid_ss}")
        logger.debug(f"'sessionid_ss' cookie updated to: {tt_target_idc}")

    def _initialize_session(self, reinitialized: bool = False) -> None:
        if hasattr(self, '_session') and self._session:
            try:
                self._session.close()
                logger.debug("Previous requests' session closed.")
            except Exception as e:
                logger.warning(f"Error closing previous requests' session: {e}")

        if reinitialized:
            logger.debug("Re-initializing requests.Session")

        self._session = requests.Session()
        self._setup_cookies()
        self._setup_proxy()
        self._session.headers.update({
            "User-Agent": self._get_random_user_agent()
        })

        logger.debug("New requests.Session initialized.")

    def _setup_cookies(self) -> None:
        sessionid_ss = self._options_handler.get_option_val(OptionKey.SESSIONID_SS)
        tt_target_idc = self._options_handler.get_option_val(OptionKey.TT_TARGET_IDC)

        assert isinstance(sessionid_ss, (str, type(None)))
        assert isinstance(tt_target_idc, (str, type(None)))

        if sessionid_ss is None and tt_target_idc is None:
            return

        if sessionid_ss:
            self._session.cookies.update({
                "sessionid_ss": sessionid_ss
            })
            logger.debug(f"'sessionid_ss' cookie set to: {sessionid_ss}")

        if tt_target_idc:
            self._session.cookies.update({
                "tt-target-idc": tt_target_idc
            })
            logger.debug(f"'tt-target-idc' cookie set to: {tt_target_idc}")

    def _setup_proxy(self) -> None:
        proxy = self._options_handler.get_option_val(OptionKey.PROXY)
        assert isinstance(proxy, (str, type(None)))

        if proxy:
            self.update_proxy(proxy)

    def _get_random_user_agent(self) -> str:
        random_ua = random.choice(USER_AGENT_LIST)

        logger.debug(f"Random User-Agent selected: {random_ua}")
        return random_ua
