import gi
from gi.repository import Gtk

from widgets.page import Page


class WatchingPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = Gtk.Box()
        self.box.append(Gtk.Label(label="OSIEM"))
        self.add_child(self.box)

    class Meta:
        name = "watching"
