from enum import StrEnum

from models.mal_model import Mal
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

    def user_anime(self, flat=False, status: Status = Status.WATCHING):
        payload = {"status": status}
        request = self.client.get(
            "users/@me/animelist?fields=list_status",
            params=payload,
        )
        data: Mal = Mal.from_payload(payload=request.json())
        if flat:
            return set([x.node.id for x in data.data])
        return data
        if flat:
            return set([x.node.id for x in data.data])
        return data
