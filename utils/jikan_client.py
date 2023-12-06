import requests

from urllib.parse import urljoin


class JikanClinet(requests.Session):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.jikan.moe/v4/"

    def request(self, method: str, url: str, *args, **kwargs):
        return super().request(
            method=method,
            url=urljoin(
                self.base_url,
                url,
            ),
            *args,
            **kwargs
        )
