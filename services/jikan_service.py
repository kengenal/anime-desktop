from typing import Optional


from models.jikan_model import Jikan
from utils.jikan_client import JikanClinet


class JikanService:
    def fetch_data(
        self,
        page: Optional[int] = None,
        query: Optional[str] = None
    ) -> Jikan:
        params = {
            "page": page,
            "q": query
        }
        client = JikanClinet()
        response = client.get(url="anime", params=params)
        return Jikan.from_payload(response.json())
