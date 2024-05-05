from typing import Generator, Optional

from models.episodes_model import Episode, EpisodeElement
from utils.x_client import XClinet


class XService:
    def __init__(self) -> None:
        self.client = XClinet()
        self.is_completed = False

    def fetch_eposodes(self, mal_id: int) -> Generator:
        is_completed = False
        while is_completed is False:
            data = self.client.get(f"/player/{str(mal_id).strip()}")
            print("Fetch all episodes", data.url)
            if data.status_code != 200:
                return None
            data = Episode.from_payload(data.json())
            is_completed = data.is_completed
            yield data.episodes

    def check(self, mal_id: int) -> bool:
        request = self.client.get(f"player/{str(mal_id)}/check")
        if request.status_code != 200:
            return False
        return request.json()["available"]

    def fetch_episode(self, mal_id: int, episode: int) -> Optional[EpisodeElement]:
        data = self.client.get(f"/player/{str(mal_id).strip()}/{str(episode)}")
        print("Get episode", data.url)
        if data.status_code != 200:
            return None

        data = Episode.from_payload(data.json())
        return data.episodes[-1]
