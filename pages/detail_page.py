from widgets.page import Page
from gi.repository import Gtk
import gi

gi.require_version('Gtk', '4.0')


class DetailPage(Page):
    def __init__(self, mal_id: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        vbox.append(Gtk.Label(label=str(mal_id)))
        vbox.append(Gtk.Label(label=str(mal_id)))
        vbox.append(hbox)
        self.append(vbox)

    class Meta:
        name = "detail"
