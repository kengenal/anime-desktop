import threading
import webbrowser
from typing import Optional

from gi.repository import Gtk

from models.episodes_model import EpisodeElement
from store.episode_store import EpisodeSotre
from store.mal_library_store import MalLibraryStore
from widgets.page import Page


class EpisodePage(Page):
    def __init__(
        self,
        mal_store: MalLibraryStore,
        episode_number: int,
        episode_store: EpisodeSotre,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args, **kwargs
        )

        self.mal_store = mal_store
        self.episode_store = episode_store
        self.episode_number = episode_number
        self.number_of_episodes = max(
            [x.episode for x in episode_store.episodes]
        )
        self.episode_source_childs = set()
        self.episode = self._get_current_episode()

        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.flow_box = Gtk.FlowBox(
            column_spacing=20,
            row_spacing=20,
            max_children_per_line=50,
            margin_end=20,
            margin_start=20,
            margin_top=20,
            margin_bottom=20,
        )
        self.box.append(self.flow_box)
        self.add_child(self.box)
        self._make_header_box()
        self._update_layaut()
        self.header_bar.set_title_widget(self.header_box)

    def on_destroy(self):
        self.header_bar.remove(child=self.header_box)

    def get_sources(self):
        self.flow_box.remove_all()
        for player in self.episode.players:
            button = Gtk.Button(label=player.source)
            button.connect("clicked", self.open_url, player.url)
            button.set_size_request(200, 100)
            self.flow_box.append(button)

    def open_url(self, _: Gtk.Button, url: str):
        webbrowser.open(url)

    def prev_episode(self, button: Gtk.Button):
        self.episode_number -= 1
        self._update_layaut()

    def next_episode(self, button: Gtk.Button):
        self.episode_number += 1
        if self.episode_number >= self.mal_store.num_watched_episodes:
            self.mal_store.num_watched_episodes = self.episode_number
        self._update_layaut()

    def _make_header_box(self):
        self.prev_button = Gtk.Button(label="PREV")
        self.next_button = Gtk.Button(label="NEXT")
        self.prev_button.connect("clicked", self.prev_episode)
        self.header_box.append(child=self.prev_button)
        self.header_box_label = Gtk.Label(
            label=str(self.episode_number), margin_start=15, margin_end=15
        )
        self.header_box.append(child=self.header_box_label)
        self.next_button.connect("clicked", self.next_episode)
        self.header_box.append(child=self.next_button)

    def _update_layaut(self) -> None:
        """
        Update next and previous button when episode number changed
        """
        self.episode = self._get_current_episode()
        self.header_box_label.set_label(str(self.episode_number))

        get_next_episode = self._get_next_episode(self.episode.episode)
        if self.episode_number == self.number_of_episodes or len(get_next_episode.players) == 0:
            self.next_button.set_visible(False)
        else:
            self.next_button.set_visible(True)

        if self.episode_number == 1:
            self.prev_button.set_visible(False)
        else:
            self.prev_button.set_visible(True)
        self.clear_stack()
        self.fetch_sources()

    def clear_stack(self):
        """
        Remove item when user go to next or prevous episode
        """
        for widget in self.episode_source_childs:
            self.stack_for_swither.remove(widget)
        self.episode_source_childs = []

    def fetch_sources(self):
        th = threading.Thread(target=self.get_sources)
        th.daemon = True
        th.start()

    def _get_next_episode(self, current_episode: int) -> Optional[EpisodeElement]:
        ep = current_episode + 1
        return next((x for x in self.episode_store.episodes if x.episode == ep), None)

    def _get_current_episode(self) -> EpisodeElement:
        return [
            x
            for x in self.episode_store.episodes
            if x.episode == self.episode_number
        ][0]

    class Meta:
        name = "episode"
