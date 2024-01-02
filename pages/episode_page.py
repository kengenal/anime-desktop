import threading
from sqlite3 import Connection, Cursor
from uuid import uuid4

from gi.repository import Gtk

from database.episode_database import EpisodeDatabase
from models.episodes_model import EpisodeElement
from services.selenium_service import SeleniumService
from store.episode_store import EpisodeSotre
from store.mal_library_store import MalLibraryStore
from widgets.page import Page
from widgets.player_widget import PlayerWidget


class EpisodePage(Page):
    def __init__(
        self,
        mal_store: MalLibraryStore,
        episode_number: int,
        episode_store: EpisodeSotre,
        db: Cursor,
        database_connection: Connection,
        *args,
        **kwargs,
    ):
        super().__init__(
            db=db, database_connection=database_connection, *args, **kwargs
        )

        self.mal_store = mal_store
        self.episode_store = episode_store
        self.episode_number = episode_number
        self.number_of_episodes = max(
            [x.episode for x in episode_store.episodes]
        )
        self.episode_source_childs = set()
        self.episode_database = EpisodeDatabase(
            db=db, database_connection=database_connection
        )
        self.selenium_is_setup = True
        self.episode = self._get_current_episode()

        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.selenium_service = SeleniumService(self.episode_database)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.spinner = Gtk.Spinner(vexpand=True, hexpand=True)

        self.stack_for_swither = Gtk.Stack()
        self.stack_switcher = Gtk.StackSwitcher(stack=self.stack_for_swither)

        self.box.append(self.spinner)
        self.box.append(self.stack_switcher)
        self.box.append(self.stack_for_swither)

        self.add_child(self.box)
        self._make_header_box()
        self._update_layaut()
        self.header_bar.set_title_widget(self.header_box)

    def on_destroy(self):
        if self.selenium_is_setup:
            self.selenium_service.quit()
        self.header_bar.remove(child=self.header_box)
        self.selenium_is_setup = False

    def on_load(self):
        if self.selenium_is_setup is False:
            self.selenium_service = SeleniumService(self.episode_database)
            self.selenium_is_setup = True

    def get_sources(self):
        self._enable_spinner()
        for episode, source in self.selenium_service.get_sources(
            self.episode, self.episode_store.mal_id
        ):
            if episode == self.episode_number:
                child = PlayerWidget(url=source.url)
                self._disable_spinner()
                self.episode_source_childs.append(child)
                self.stack_for_swither.add_titled(
                    child=child,
                    name=f"{source.source}-{source.player_source}-{str(uuid4())}",
                    title=f"{source.source} {source.player_source} {episode}",
                )

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

    def _enable_spinner(self):
        self.spinner.set_visible(True)
        self.spinner.set_spinning(True)

    def _disable_spinner(self):
        self.spinner.set_visible(False)
        self.spinner.set_spinning(False)

    def _update_layaut(self) -> None:
        """
        Update next and previous button when episode number changed
        """
        self.episode = self._get_current_episode()
        self.header_box_label.set_label(str(self.episode_number))

        if self.episode_number == self.number_of_episodes:
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

    def _get_current_episode(self) -> EpisodeElement:
        return [
            x
            for x in self.episode_store.episodes
            if x.episode == self.episode_number
        ][0]

    class Meta:
        name = "episode"
