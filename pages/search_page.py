from gi.repository import Gtk

from widgets.page import Page


class SearchPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search = Gtk.SearchEntry()

        button = Gtk.Button(label="Change")
        button.connect("clicked", self.change_direction)
        button.set_halign(align=Gtk.Align.CENTER)
        button.set_valign(align=Gtk.Align.CENTER)
        button.set_hexpand(expand=True)
        button.set_vexpand(expand=True)
        self.append(button)
        self.on_load()

    def change_direction(self, *args, **kwargs):
        pass

    def on_load(self):
        self.header_bar.pack_start(self.search)

    def on_destroy(self):
        self.header_bar.remove(self.search)

    class Meta:
        name = "search"
