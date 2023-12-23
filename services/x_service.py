from typing import Generator
import time
from models.episodes_model import Episode
from utils.x_client import XClinet


class XService:
    def __init__(self) -> None:
        self.client = XClinet()
        self.is_completed = False

    def fetch_eposodes(self, mal_id: int) -> Generator:
        is_completed = False
        while is_completed is False:
            data = self.client.get(f"/player/{str(mal_id)}")
            if data.status_code != 200:
                return None
            data = Episode.from_payload(data.json())
            is_completed = data.is_completed
            yield data.episodes
