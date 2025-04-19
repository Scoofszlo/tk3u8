import requests
from tk3u8.config import Config
from tk3u8.constants import Cookie
from tk3u8.custom_exceptions import InvalidCookieError, RequestFailedError


class RequestHandler:
    def __init__(self, config: Config):
        self.session = requests.Session()
        self.config = config
        self._update_cookies()
        self.session.headers.update({
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
        self.response: requests.Response

    def get_data(self, username) -> requests.Response:
        self.response = self.session.get(f"https://www.tiktok.com/@{username}/live")

        if self.response.status_code != 200:
            raise RequestFailedError(status_code=self.response.status_code)

        return self.response

    def _update_cookies(self) -> None:
        sessionid_ss = self.config.get_config(Cookie.SESSIONID_SS)
        tt_target_idc = self.config.get_config(Cookie.TT_TARGET_IDC)

        if sessionid_ss is None and tt_target_idc is None:
            return
        elif sessionid_ss is None and tt_target_idc is not None:
            raise InvalidCookieError("The 'tt-target-idc' cookie is set in your config, but 'sessionid_ss' is missing.")
        elif sessionid_ss is not None and tt_target_idc is None:
            raise InvalidCookieError("The 'sessionid_ss' cookie is set in your config, but 'tt-target-idc' is missing.")
        elif sessionid_ss and tt_target_idc:
            self.session.cookies.update({
                "sessionid_ss": sessionid_ss,
                "tt-target-idc": tt_target_idc
            })
