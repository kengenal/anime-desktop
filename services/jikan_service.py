from typing import Optional


from models.jikan_model import Jikan, Datum
from utils.jikan_client import JikanClinet


class JikanService:
    def __init__(self):
        self.client = JikanClinet()

    def fetch_data(self, page: int = 1, query: Optional[str] = None) -> Jikan:
        params = {"page": page, "q": "spy x family"}
        response = self.client.get(url="anime", params=params)
        return Jikan.from_payload(response.json())

    def get_by_id(self, mal_id: int) -> Datum:
        response = self.client.get(url=f"anime/{str(mal_id)}/full")
        data = response.json().get("data")
        return Datum.from_payload(data)
