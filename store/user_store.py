from typing import Dict, Optional, Set

from dill import copy
from gi.repository import GObject

from services.mal_service import Status
from utils.compare import compare_and_get_keys


class UserStore(GObject.Object):
    __gsignals__ = {
        "value-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
        "user-library-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
        "watch-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
        "completed-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
        "plantowatch-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
        "dropped-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
    }

    def __init__(self):
        super().__init__()
        self._is_login = False
        self._watching_anime_ids = {
            Status.WATCHING: set(),
            Status.COMPLETED: set(),
            Status.ON_HOLD: set(),
            Status.PLAN_TO_WATCH: set(),
            Status.DROPPED: set(),
        }

    @property
    def user_anime_ids(self) -> Set:
        return self._watching_anime_ids

    @user_anime_ids.setter
    def user_anime_ids(self, new_value: Dict[Status, Set]) -> None:
        if new_value != self._watching_anime_ids:
            self._call_signals(
                updated=compare_and_get_keys(
                    d1=new_value, d2=self._watching_anime_ids
                )
            )
            self._watching_anime_ids = new_value
            self.emit("user-library-update", "user_anime_ids", new_value)

    @property
    def is_login(self) -> bool:
        return self._is_login

    @is_login.setter
    def is_login(self, new_value) -> None:
        if new_value != self._is_login:
            self._is_login = new_value
            self.emit("value-changed", "is_login", new_value)

    def update_user_anime(
        self, prev_status: Optional[Status], new_status: Status, mal_id: int
    ):
        data = copy(self._watching_anime_ids)
        data[new_status].add(mal_id)
        if prev_status:
            data[prev_status].remove(mal_id)
        self.user_anime_ids = data

    def _call_signals(self, updated: Set[Status]) -> None:
        for upd in updated:
            match upd:
                case Status.WATCHING:
                    self.emit(
                        "watch-update",
                        "user_anime_ids",
                        self._watching_anime_ids,
                    )
                case Status.PLAN_TO_WATCH:
                    self.emit(
                        "plantowatch-update",
                        "user_anime_ids",
                        self._watching_anime_ids,
                    )
                case Status.COMPLETED:
                    self.emit(
                        "completed-update",
                        "user_anime_ids",
                        self._watching_anime_ids,
                    )
                case Status.DROPPED:
                    self.emit(
                        "dropped-update",
                        "user_anime_ids",
                        self._watching_anime_ids,
                    )
