from gi.repository import Gio, GLib, Gtk

from models.episodes_model import Player


class PlayerWidget(Gtk.Box):
    def __init__(self, url: str, *args, **kwargs):
        self.url = url
        print(url)
        super().__init__(*args, **kwargs)
        GLib.idle_add(self.load)

    def load(self):
        file = Gio.file_new_for_uri(self.url)
        self.player = Gtk.Video(
            vexpand=True,
            hexpand=True,
            margin_bottom=20,
            margin_end=20,
            margin_start=20,
            margin_top=20,
        )
        self.player.set_file(file=file)

        self.append(child=self.player)
