from typing import List, Optional

from gi.repository import GObject

from models.mal_model import Datum
from services.mal_service import Status


class MalLibraryStore(GObject.Object):
    __gsignals__ = {
        "watched-episodes-changed": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
        "status-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
        "list-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
    }

    def __init__(self) -> None:
        super().__init__()
        self._num_watched_episodes = 0
        self._status = None
        self._prev_status = None
        self._mal_anime_info = None
        self._user_anime_list = []
        self._user_list_history = []

    @property
    def user_anime_list(self) -> List[Datum]:
        return self._user_anime_list

    @user_anime_list.setter
    def user_anime_list(self, new_value: List[Datum]):
        if len(new_value) != len(self._user_anime_list):
            self._user_list_history = self._user_anime_list
            self._user_anime_list = new_value
            self.emit("list-changed", "user_anime_list", new_value)

    @property
    def mal_anime_info(self) -> Optional[Datum]:
        return self._mal_anime_info

    @mal_anime_info.setter
    def mal_anime_info(self, anime_info: Optional[Datum]):
        if anime_info != self._mal_anime_info:
            self._status = Status[anime_info.list_status.status.upper()]
            self._num_watched_episodes = int(
                anime_info.list_status.num_episodes_watched
            )
            self.emit("status-changed", "status", self._status)
            self.emit(
                "watched-episodes-changed",
                "num_watched_episodes",
                self._num_watched_episodes,
            )

    @property
    def status(self) -> Optional[Status]:
        return self._status

    @status.setter
    def status(self, status: Status) -> None:
        if status != self._status:
            self._prev_status = self.status
            self._status = status
            self.emit("status-changed", "status", status)

    @property
    def prev_status(self) -> Optional[Status]:
        return self._prev_status

    @property
    def num_watched_episodes(self) -> int:
        return self._num_watched_episodes

    @num_watched_episodes.setter
    def num_watched_episodes(self, new_value: int) -> None:
        if new_value != self._num_watched_episodes:
            self._num_watched_episodes = new_value
            self.emit(
                "watched-episodes-changed", "num_watched_episodes", new_value
            )
