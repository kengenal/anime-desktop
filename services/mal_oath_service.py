import os
from typing import Tuple
from urllib.parse import urlencode
from webbrowser import open

import requests
from dotenv import load_dotenv

from exceptions.mal_exceptions import MalLoginException
from utils.pkce import PKCE


class MalOath2Service:
    def __init__(self):
        self.authorize_url = "https://myanimelist.net/v1/oauth2/authorize"
        self.token_url = "https://myanimelist.net/v1/oauth2/token"
        (
            self.code_verifier,
            self.code_verifier_length,
        ) = PKCE.code_verifier()
        load_dotenv()
        self.callback_url = "http://localhost:3000"
        self.client_id = os.getenv("client_id")
        self.client_secret = os.getenv("client_secret")

    def authorize(self):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "state": "",
            "redirect_uri": self.callback_url,
            "code_challenge": self.code_verifier,
            "scope": "write:users,",
        }
        url = self.authorize_url + "?" + urlencode(params)
        open(url)

    def fetch_token(self, code: str) -> Tuple[str, str]:
        prepere_data = {
            "client_id": self.client_id,
            "code": code,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": self.callback_url,
            "code_verifier": self.code_verifier,
        }

        request = requests.post(
            self.token_url,
            prepere_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        if request.status_code != 200:
            raise MalLoginException()
        return request.json()["access_token"], request.json()["refresh_token"]
