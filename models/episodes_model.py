from dataclasses import dataclass
from typing import Dict, List

from dacite import from_dict


@dataclass
class Player:
    url: str
    source: str
    type: str
    player_source: str


@dataclass
class EpisodeElement:
    episode: int
    name: str
    players: List[Player]
    lang: str


@dataclass
class Episode:
    id: int
    is_completed: bool
    episodes: List[EpisodeElement]

    @staticmethod
    def from_payload(payload: Dict):
        return from_dict(data_class=Episode, data=payload)
