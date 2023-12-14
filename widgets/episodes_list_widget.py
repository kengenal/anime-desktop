
from typing import List

from models.episodes_model import EpisodeElement

from gi.repository import Gtk
from widgets.page import Page


class EpisodesListWidget(Gtk.Box):
    def __init__(self, go_to , *args, **kwargs) -> None:
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.go_to = go_to
 
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
            button.connect("clicked", self.go_to, episode.episode)
            self.flow_box.append(child=button)

    def _go_to_episode(self, _: Gtk.Button, episode_number: int):
        destination = self.page(
            episode_number=episode_number,
            **self.to_inject
        )
        self.stack.add_named(child=destination, name=self.page.Meta.name)
        self.stack.set_visible_child(destination)