import requests
from urllib.parse import urljoin


class XClinet(requests.Session):
    def __init__(self) -> None:
        super().__init__()
        self.base_url = "http://127.0.0.1:5000/"

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
