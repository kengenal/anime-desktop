from dataclasses import dataclass
from typing import Dict, List

from dacite.core import from_dict


@dataclass
class ListStatus:
    status: str
    score: int
    num_episodes_watched: int
    is_rewatching: bool
    updated_at: str


@dataclass
class MainPicture:
    medium: str
    large: str


@dataclass
class Node:
    id: int
    title: str
    main_picture: MainPicture


@dataclass
class Datum:
    node: Node
    list_status: ListStatus


@dataclass
class Paging:
    pass


@dataclass
class Mal:
    data: List[Datum]
    paging: Paging

    @staticmethod
    def from_payload(payload: Dict):
        return from_dict(data_class=Mal, data=payload)
