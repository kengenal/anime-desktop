from enum import StrEnum
from typing import Optional

from models.mal_model import Datum, Mal
from utils.mal_client import MalClient


class Status(StrEnum):
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLAN_TO_WATCH = "plan_to_watch"


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
