from models.episodes_model import Player

from gi.repository import Gtk, Gio

class PlayerWidget(Gtk.Box):
    def __init__(self, player_url: Player ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        file = Gio.file_new_for_uri("https://download.blender.org/peach/trailer/trailer_400p.ogg")
        player = Gtk.Video(
            vexpand=True,
            hexpand=True,
            margin_bottom=20,
            margin_end=20,
            margin_start=20,
            margin_top=20
        )
        player.set_file(file=file)

        self.append(child=player)
