from gi.repository import Gtk

from models.mal_model import Node
from widgets.network_image import AsyncImage


class CardLibWidget(Gtk.Box):
    def __init__(self, anime: Node, *args, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        image = AsyncImage(url=anime.main_picture.large)

        image.set_vexpand(True)
        image.set_hexpand(True)

        image.set_css_classes(["img"])
        title = Gtk.Label(
            label=anime.title,
            css_classes=["card-title"],
            wrap=True,
        )
        self.append(image)
        self.append(title)
