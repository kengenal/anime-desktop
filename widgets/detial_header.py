

import gi

from models.jikan_model import Datum
from widgets.network_image import AsyncImage

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk


class DetalHeader(Gtk.Box):
    def __init__(self, anime: Datum) -> None:
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) 
        title = Gtk.Label(
            label=anime.title,
            justify=Gtk.Justification.CENTER,
            selectable=True,
        )
        description = Gtk.Label(
            selectable=True,
            wrap=True,
            label=anime.synopsis or "",
            hexpand=True,
            justify=Gtk.Justification.CENTER
        )
        
        title.set_size_request(100, 100)
        
        vbox.append(title)
        vbox.append(description)
        vbox.set_margin_start(50)
        if anime.images and anime.images.jpg and  anime.images.jpg.large_image_url:
            image = AsyncImage(anime.images.jpg.large_image_url)
            image.set_size_request(300, 300)
            self.append(image)
        self.append(vbox)
