import requests
from tk3u8.constants import OptionKey
from tk3u8.exceptions import RequestFailedError
from tk3u8.options_handler import OptionsHandler


class RequestHandler:
    def __init__(self, options_handler: OptionsHandler) -> None:
        self._options_handler = options_handler
        self._session = requests.Session()
        self._setup_cookies()
        self._setup_proxy()
        self._session.headers.update({
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"",
            "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Linux\"",
            "Accept-Language": "en-US", "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document",
            "Priority": "u=0, i",
            "Referer": "https://www.tiktok.com/"
        })
        self._response: requests.Response

    def get_data(self, username) -> requests.Response:
        self._response = self._session.get(f"https://www.tiktok.com/@{username}/live")

        if self._response.status_code != 200:
            raise RequestFailedError(status_code=self._response.status_code)

        return self._response

    def update_proxy(self, proxy: str | None) -> None:
        if proxy:
            self._session.proxies.update({
                    "http": proxy,
                    "https": proxy
            })

    def _setup_cookies(self) -> None:
        sessionid_ss = self._options_handler.get_arg_val(OptionKey.SESSIONID_SS)
        tt_target_idc = self._options_handler.get_arg_val(OptionKey.TT_TARGET_IDC)

        assert isinstance(sessionid_ss, (str, type(None)))
        assert isinstance(tt_target_idc, (str, type(None)))

        if sessionid_ss is None and tt_target_idc is None:
            return
        if sessionid_ss:
            self._session.cookies.update({
                "sessionid_ss": sessionid_ss
            })
        if tt_target_idc:
            self._session.cookies.update({
                "tt-target-idc": tt_target_idc
            })

    def _setup_proxy(self) -> None:
        proxy = self._options_handler.get_arg_val(OptionKey.PROXY)
        assert isinstance(proxy, (str, type(None)))

        if proxy:
            self.update_proxy(proxy)
