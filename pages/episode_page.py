import sqlite3
import threading
from sqlite3 import Connection, Cursor
from uuid import uuid4

from gi.repository import GLib, Gtk

from database.episode_database import EpisodeDatabase
from models.episodes_model import Player
from services.selenium_service import SeleniumService
from store.episode_store import EpisodeSotre
from widgets.page import Page
from widgets.player_widget import PlayerWidget


class EpisodePage(Page):
    def __init__(
        self,
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
        self.episode_database = EpisodeDatabase(
            db=db, database_connection=database_connection
        )

        self.selenium_service = SeleniumService(self.episode_database)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.prev_button = Gtk.Button(label="PREV")
        self.next_button = Gtk.Button(label="NEXT")
        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.header_box.append(child=self.next_button)
        self.header_box.append(
            child=Gtk.Label(
                label=str(episode_number), margin_start=15, margin_end=15
            )
        )
        self.header_box.append(child=self.prev_button)

        self.stack_for_swither = Gtk.Stack()
        self.stack_switcher = Gtk.StackSwitcher(stack=self.stack_for_swither)
        self.box.append(self.stack_switcher)
        self.box.append(self.stack_for_swither)

        self.add_child(self.box)

        self.episode_store = episode_store
        self.episode = [
            x
            for x in episode_store.episodes
            if episode_number == episode_number
        ][0]
        th = threading.Thread(target=self.get_sources)
        th.daemon = True
        th.start()

        self.header_bar.set_title_widget(self.header_box)

    def on_destroy(self):
        self.header_bar.remove(child=self.header_box)

    def get_sources(self):
        for source in self.selenium_service.get_sources(
            self.episode, self.episode_store.mal_id
        ):
            self.stack_for_swither.add_titled(
                child=PlayerWidget(url=source.url),
                name=f"{source.source}-{source.player_source}",
                title=f"{source.source}-{source.player_source}",
            )

    class Meta:
        name = "episode"
