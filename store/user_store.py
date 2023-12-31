from typing import Set

from gi.repository import GObject


class UserStore(GObject.Object):
    __gsignals__ = {
        "value-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
        "user-library-update": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, bool),
        ),
    }

    def __init__(self):
        super().__init__()
        self._is_login = False
        self._watching_anime_ids = set()

    @property
    def watching_anime_ids(self) -> Set:
        return self._watching_anime_ids

    @watching_anime_ids.setter
    def watching_anime_ids(self, new_value: Set) -> None:
        self._watching_anime_ids = new_value
        self.emit("user-library-update", "watching_anime_ids", new_value)

    @property
    def is_login(self) -> bool:
        return self._is_login

    @is_login.setter
    def is_login(self, new_value) -> None:
        if new_value != self._is_login:
            self._is_login = new_value
            self.emit("value-changed", "is_login", new_value)
