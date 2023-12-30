from models.mal_model import Mal
from utils.mal_client import MalClient


class MalService:
    def __init__(self):
        self.client = MalClient()

    def user_anime(self, flat=False):
        request = self.client.get("users/@me/animelist?fields=list_status")
        data: Mal = Mal.from_payload(payload=request.json())
        if flat:
            return set([x.node.id for x in data.data])
        return data
