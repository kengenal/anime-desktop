from dataclasses import asdict
from typing import Optional

from const.mal import Status
from exceptions.mal_exceptions import MalApiException
from models.mal_model import Datum, Mal, MalAnimeUpdate
from utils.mal_client import MalClient


class MalService:
    def __init__(self):
        self.client = MalClient()

    def user_anime(self, flat=False, status: Status = None) -> Mal:
        payload = {}
        if status:
            payload["status"] = status
        request = self.client.get(
            "users/@me/animelist?fields=list_status",
            params=payload,
        )
        data: Mal = Mal.from_payload(payload=request.json())
        return data
        if flat:
            return set([x.node.id for x in data.data])
        return data

    def get_possition_by_mal_id(self, mal_id: int) -> Optional[Datum]:
        res = self.user_anime()
        fetch_res = [x for x in res.data if x.node.id == mal_id]
        if fetch_res:
            return fetch_res[0]
        return None

    def update_possition(self, mal_id: int, payload: MalAnimeUpdate):
        to_dict = {k: v for k, v in asdict(payload).items() if v is not None}
        request = self.client.patch(
            f"anime/{mal_id}/my_list_status",
            to_dict,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if request.status_code != 401 and request.status_code != 200:
            raise MalApiException(status_code=request.status_code)

    def delete_anime_from_lib(self, mal_id: int):
        request = self.client.delete(
            f"anime/{mal_id}/my_list_status",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        if request.status_code != 401 and request.status_code != 200:
            raise MalApiException(status_code=request.status_code)
