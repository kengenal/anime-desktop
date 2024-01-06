from dataclasses import dataclass
from typing import Dict, List, Optional

from dacite.core import from_dict

from const.mal import Status


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


@dataclass
class MalAnimeUpdate:
    status: Optional[Status] = None
    is_rewatching: Optional[bool] = None
    score: Optional[int] = None
    num_watched_episodes: Optional[int] = None
    priority: Optional[int] = None
    num_times_rewatched: Optional[int] = None
    rewatch_value: Optional[int] = None
    tags: Optional[str] = None
    comments: Optional[str] = None
