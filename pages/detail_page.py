import gi
import threading
from gi.repository import Gtk
from models.episodes_model import EpisodeElement

from services.jikan_service import JikanService
from services.x_service import XService
from store.episode_store import EpisodeSotre
from widgets.detial_header import DetalHeader
from widgets.episodes_list_widget import EpisodesListWidget
from widgets.page import Page



class DetailPage(Page):
    def __init__(self, mal_id: int, header_bar: Gtk.HeaderBar, *args, **kwargs):
        super().__init__(header_bar=header_bar, *args, **kwargs)

        self.box = Gtk.Box()
        self.mal_id = mal_id
        self.jikan_service = JikanService()
        self.stack_for_switcher = Gtk.Stack()
        self.stack_for_switcher.props.transition_type = Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        self.stack_switcher = Gtk.StackSwitcher(stack=self.stack_for_switcher)

        header_bar.set_title_widget(self.stack_switcher)


        self.episode_store = EpisodeSotre()
        self.episode_store.connect("value-changed", self.set_episodes)
        
        self.episode_widget = EpisodesListWidget()
        button = Gtk.Button(label="Fetch data")
        self.episode_widget.append(button)
        button.connect("clicked", self.load_pisodes)
        

        self.info_page = Gtk.Box()
        
        self.stack_for_switcher.add_titled(child=self.info_page, name="info", title="Info")
        self.stack_for_switcher.add_titled(child=self.episode_widget, name="episodes", title="Episodes")
        self.add_child(self.stack_for_switcher)
        self.x_service = XService()

  
        threading.Thread(target=self.load_anime, daemon=True).start()

    def on_destroy(self):
        self.header_bar.remove(child=self.stack_switcher)

    def load_anime(self):
        data = self.jikan_service.get_by_id(self.mal_id)
        self.info_page.append(child=DetalHeader(anime=data))

    def set_episodes(self, *args, **kwargs):
        self.episode_widget.set_episodes(self.episode_store.episodes)
    
    def load_pisodes(self, *args, **kwargs):
        threading.Thread(target=self._load_episodes, daemon=True).start()

    def _load_episodes(self):
        for episodes in self.x_service.fetch_eposodes(self.mal_id):
            if episodes is None:
                return
            self.episode_store.episodes = episodes


    class Meta:
        name = "detail"
