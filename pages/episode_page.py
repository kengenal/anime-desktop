from ast import Dict
from typing import List
import gi

from gi.repository import Gtk
from store.episode_store import EpisodeSotre
from widgets.page import Page
from widgets.player_widget import PlayerWidget


class EpisodePage(Page):
    def __init__(self, episode_number: int, episode_store: EpisodeSotre, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.prev_button = Gtk.Button(label="PREV")
        self.next_button = Gtk.Button(label="NEXT")
        self.header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        
        self.header_box.append(child=self.next_button)
        self.header_box.append(child=Gtk.Label(label=str(episode_number), margin_start=15, margin_end=15))
        self.header_box.append(child=self.prev_button)


        self.stack_for_swither = Gtk.Stack()
        self.episode_store = episode_store
        self.episode = [x for x in episode_store.episodes if episode_number == episode_number][0]
        
        self.stack_switcher = Gtk.StackSwitcher(stack=self.stack_for_swither)
        for player in self.episode.players:
            self.stack_for_swither.add_titled(
                child=PlayerWidget(player_url=player.url), 
                name=player.source.lower(), 
                title=player.source
            )
   
        self.box.append(self.stack_switcher)
        self.box.append(self.stack_for_swither)

        self.add_child(self.box)

        self.header_bar.set_title_widget(self.header_box)

    def on_destroy(self):
        self.header_bar.remove(child=self.header_box)

    class Meta:
        name = "episode"
