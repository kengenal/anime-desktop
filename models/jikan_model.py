from dataclasses import dataclass
from typing import Optional, Dict, List, Any

from dacite import from_dict


@dataclass
class From:
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None


@dataclass
class Prop:
    prop_from: Optional[From] = None
    to: Optional[From] = None


@dataclass
class Aired:
    aired_from: Optional[str] = None
    to: Optional[str] = None
    prop: Optional[Prop] = None
    string: Optional[str] = None


@dataclass
class Broadcast:
    day: Optional[str] = None
    time: Optional[str] = None
    timezone: Optional[str] = None
    string: Optional[str] = None


@dataclass
class Demographic:
    mal_id: Optional[int] = None
    name: Optional[str] = None
    url: Optional[str] = None


@dataclass
class Jpg:
    image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    large_image_url: Optional[str] = None


@dataclass
class Image:
    jpg: Optional[Jpg]


@dataclass
class Title:
    title: Optional[str] = None


@dataclass
class Images:
    image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    medium_image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    maximum_image_url: Optional[str] = None


@dataclass
class Trailer:
    youtube_id: Optional[str] = None
    url: Optional[str] = None
    embed_url: Optional[str] = None
    images: Optional[Images] = None


@dataclass
class Datum:
    mal_id: int
    title: str
    url: Optional[str] = None
    images: Optional[Image] = None
    trailer: Optional[Trailer] = None
    approved: Optional[bool] = None
    titles: Optional[List[Title]] = None
    title_english: Optional[str] = None
    title_japanese: Optional[str] = None
    title_synonyms: Optional[List[str]] = None
    type: Optional[str] = None
    episodes: Optional[int] = None
    airing: Optional[bool] = None
    aired: Optional[Aired] = None
    duration: Optional[str] = None
    score: Optional[float] = None
    scored_by: Optional[int] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None
    members: Optional[int] = None
    favorites: Optional[int] = None
    synopsis: Optional[str] = None
    background: Optional[str] = None
    season: Optional[str] = None
    year: Optional[int] = None
    broadcast: Optional[Broadcast] = None
    producers: Optional[List[Demographic]] = None
    licensors: Optional[List[Demographic]] = None
    studios: Optional[List[Demographic]] = None
    genres: Optional[List[Demographic]] = None
    explicit_genres: Optional[List[Any]] = None
    themes: Optional[List[Demographic]] = None
    demographics: Optional[List[Demographic]] = None

    @staticmethod
    def from_payload(payload: Dict):
        return from_dict(data_class=Datum, data=payload)


@dataclass
class Items:
    count: Optional[int] = None
    total: Optional[int] = None
    per_page: Optional[int] = None


@dataclass
class Pagination:
    last_visible_page: Optional[int] = None
    has_next_page: Optional[bool] = None
    current_page: Optional[int] = None
    items: Optional[Items] = None


@dataclass
class Jikan:
    pagination: Pagination
    data: List[Datum]

    @staticmethod
    def from_payload(payload: Dict):
        return from_dict(data_class=Jikan, data=payload)
