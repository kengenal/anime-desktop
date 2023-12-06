import gi
from typing import Dict
from gi.repository import GLib, Gtk
from models.episodes_model import EpisodeElement

from services.jikan_service import JikanService
from services.x_service import XService
from store.episode_store import EpisodeSotre
from widgets.detial_header import DetalHeader
from widgets.episodes_list_widget import EpisodesListWidget
from widgets.page import Page



class DetailPage(Page):
    def __init__(self, mal_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mal_id = mal_id
        self.jikan_service = JikanService()

        self.x_service = XService()
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.scroll_view.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scroll_view.set_child(self.vbox)
        self.append(self.scroll_view)
        self.episode_store = EpisodeSotre()
        self.episode_store.connect("value-changed", self.set_episodes)
        self.button = Gtk.Button(label="Fetch data")
        self.button.connect("clicked", self.load_pisodes)
        self.episode_widget = EpisodesListWidget()
        self.vbox.append(self.button)
        GLib.idle_add(self.load_anime)

    def load_anime(self):
        data = self.jikan_service.get_by_id(self.mal_id)
        self.vbox.append(child=DetalHeader(anime=data))
        self.vbox.append(self.episode_widget)

    def set_episodes(self, *args, **kwargs):
        self.episode_widget.set_episodes(self.episode_store.episodes)
    
    def load_pisodes(self, *args, **kwargs):
        GLib.idle_add(self._load_episode)

    def _load_episode(self):
        for episodes in self.x_service.fetch_eposodes(self.mal_id):
            if episodes is None:
                return
            self.episode_store.episodes = episodes


    class Meta:
        name = "detail"
