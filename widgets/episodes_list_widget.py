from datetime import datetime
from typing import List, Optional

from gi.repository import Gtk

from models.episodes_model import EpisodeElement
from store.episode_store import EpisodeSotre
from store.mal_library_store import MalLibraryStore


class EpisodesListWidget(Gtk.Box):
    def __init__(
        self,
        mal_store: MalLibraryStore,
        episode_store: EpisodeSotre,
        go_to,
        get_episode,
        *args,
        **kwargs
    ) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.mal_store = mal_store
        self.go_to = go_to
        self.get_episode = get_episode

        self.spinner = Gtk.Spinner(hexpand=True, vexpand=True, visible=True)
        self.episode_not_found_label = Gtk.Label(
            label="""
                Episode not found, add to watch
            """,
            hexpand=True,
            vexpand=True,
            visible=False,
        )
        self.append(self.episode_not_found_label)
        self.append(self.spinner)
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)

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
        self.scroll_view.set_child(child=self.flow_box)
        self.append(self.scroll_view)

    def set_episodes(self, episodes: int, available_episodes: List[EpisodeElement]):
        self.flow_box.remove_all()
        if len(available_episodes) > 1:
            for episode in range(1, episodes + 1):
                episode_info: Optional[List[EpisodeElement]] = next(
                    (x for x in available_episodes if x.episode == episode), None
                )

                button = Gtk.Button(
                    label=str(episode),
                    css_classes=["card-button", "ctitle"],
                    height_request=300,
                    width_request=300,
                    name=str(episode),
                )
                is_episode_is_available = False

                if (
                    episode_info
                    and len(episode_info.players) > 0
                    and episode_info.is_translated is True
                ):
                    is_episode_is_available = True

                if episode <= self.mal_store.num_watched_episodes:
                    button.add_css_class("watched-button")

                if episode_info:
                    button.connect("clicked", self.go_to, episode)

                if is_episode_is_available is False:
                    button.set_sensitive(False)

                if is_episode_is_available is False:
                    self._check_if_episode_to_fetch(
                        episode=episode, release_date=episode_info.release_date
                    )

                self.flow_box.append(child=button)

    def start_loading(self):
        self.spinner.set_visible(True)

    def end_loading(self):
        self.spinner.set_spinning(False)
        self.episode_not_found_label.set_visible(False)

        self.spinner.set_visible(False)

    def set_label(self):
        self.spinner.set_spinning(True)
        self.episode_not_found_label.set_visible(True)

    def remove_label(self):
        self.episode_not_found_label.set_visible(False)

    def _go_to_episode(self, _: Gtk.Button, episode_number: int):
        destination = self.page(episode_number=episode_number, **self.to_inject)
        self.stack.add_named(child=destination, name=self.page.Meta.name)
        self.stack.set_visible_child(destination)

    def _check_if_episode_to_fetch(
        self, episode: int, release_date: Optional[datetime]
    ):
        if not release_date:
            self.get_episode(episode)
            return
        release_date = datetime.fromisoformat(release_date).replace(tzinfo=None)
        now = datetime.now().replace(tzinfo=None)
        if release_date < now:
            self.get_episode(episode)
