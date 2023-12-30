import os
from typing import Dict
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
from requests import Request

from exceptions.mal_exceptions import MalAuthorizationException
from utils.pkce import PKCE
from utils.secure_store import SecureStore


class MalClient(requests.Session):
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.myanimelist.net/v2/"
        self.refresh_token_url = "https://myanimelist.net/v1/oauth2/token"
        self.secure_store = SecureStore()
        load_dotenv()
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")

    def request(self, method: str, url: str, *args, **kwargs) -> Request:
        payload = {
            "method": method,
            "url": urljoin(self.base_url, url),
            "headers": kwargs.pop("headers", {}),
        }
        payload.update(kwargs)
        token = self.secure_store.get("token")
        if not token:
            raise MalAuthorizationException()

        payload["headers"]["Authorization"] = f"Bearer {token}"
        request = super().request(**payload)
        if request.status_code == 401:
            return self._refresh_token(payload=payload)

        if request.status_code == 403:
            self.secure_store.delete("token")
            self.secure_store.delete("refresh_token")
            raise MalAuthorizationException()
        return request

    def _refresh_token(self, payload: Dict) -> Request:
        code_verifier = PKCE.code_verifier()
        refresh_token = self.secure_store.get("refresh_token")

        request_data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code_verifier": code_verifier,
        }

        request = requests.post(
            self.refresh_token_url,
            request_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if request.status_code == 200:
            self.secure_store.set("token", request.json().get("access_token"))
            self.secure_store.set(
                "refresh_token", request.json().get("refresh_token")
            )
            return self.request(**payload)

        raise MalAuthorizationException()
