from typing import List
import gi
from models.episodes_model import EpisodeElement

from gi.repository import Gtk


class EpisodesListWidget(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)

        self.append(self.scroll_view)

        self.flow_box = Gtk.FlowBox(
            column_spacing=20,
            row_spacing=20,
            max_children_per_line=50,
            margin_end=20,
            margin_start=20,
            margin_top=20,
            margin_bottom=20,

        )
        self.flow_box.set_column_spacing(20)

        self.flow_box.set_max_children_per_line(50)
        self.scroll_view.set_child()
        self.spinner = Gtk.Spinner(hexpand=True, vexpand=True)
        self.append(self.spinner)
        self.scroll_view.set_child(child=self.flow_box)

    def set_episodes(self, episodes: List[EpisodeElement]):
        self.remove(self.spinner)
        self.flow_box.remove_all()
        for episode in episodes:
            button = Gtk.Button(
                label=str(episode.episode),
                css_classes=["card-button", "ctitle"],
                height_request=300,
                width_request=300
            )

            self.flow_box.append(child=button)
