from typing import Optional
import requests

from tk3u8.custom_exceptions import RequestFailedError


class RequestHandler:
    def __init__(self):
        self.session = requests.Session()
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
        self.response: Optional[requests.Response] = None

    def get_data(self, username) -> requests.Response:
        self.response = self.session.get(f"https://www.tiktok.com/@{username}/live")

        if self.response.status_code != 200:
            raise RequestFailedError(status_code=self.response.status_code)

        return self.response
