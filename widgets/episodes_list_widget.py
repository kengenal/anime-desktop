from typing import List
import gi
from models.episodes_model import EpisodeElement

from gi.repository import Gtk


class EpisodesListWidget(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL, hexpand=True)
        
        self.flow_box = Gtk.FlowBox(hexpand=True)
        self.flow_box.set_column_spacing(20)

        self.flow_box.set_max_children_per_line(50)
        self.spinner = Gtk.Spinner(hexpand=True, vexpand=True)
        self.append(self.spinner)
        self.append(child=self.flow_box)

    def set_episodes(self, episodes: List[EpisodeElement]):
        self.remove(self.spinner)
        self.flow_box.remove_all()
        for episode in episodes:
            button = Gtk.Button(label=str(episode.episode))
            button.set_size_request(300, 300)
            self.flow_box.append(child=button)
