import gi
from gi.repository import GLib, Gtk

from services.jikan_service import JikanService
from widgets.detial_header import DetalHeader
from widgets.page import Page

gi.require_version("Gtk", "4.0")


class DetailPage(Page):
    def __init__(self, mal_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mal_id = mal_id
        self.jikan_service = JikanService()
        self.scroll_view = Gtk.ScrolledWindow()
        self.scroll_view.set_vexpand(True)
        self.scroll_view.set_hexpand(True)
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.scroll_view.set_child(self.vbox)
        self.append(self.scroll_view)
        GLib.idle_add(self.load_anime)

    def load_anime(self):
        data = self.jikan_service.get_by_id(self.mal_id)
        self.vbox.append(child=DetalHeader(anime=data))

    class Meta:
        name = "detail"
