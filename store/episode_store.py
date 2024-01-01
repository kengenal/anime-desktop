from typing import List

from gi.repository import GObject

from models.episodes_model import EpisodeElement


class EpisodeSotre(GObject.Object):
    __gsignals__ = {
        "value-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
    }

    def __init__(self, mal_id: int) -> None:
        super().__init__()
        self.mal_id = mal_id
        self._episodes = []

    @property
    def episodes(self) -> List[EpisodeElement]:
        return self._episodes

    @episodes.setter
    def episodes(self, new_value: List[EpisodeElement]):
        if new_value != self._episodes:
            self._episodes = new_value
            self.emit("value-changed", "episodes", new_value)
