from typing import Dict, Optional

import gi

from models.jikan_model import Datum
from widgets.network_image import AsyncImage


from gi.repository import Gtk


class CardSearchWidget(Gtk.Box):
    def __init__(self, anime: Datum, *args, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_top(12)
        image = AsyncImage(url=anime.images.jpg.large_image_url)
        image.set_size_request(300, 300)
        self.append(image)
        self.append(Gtk.Label(label=anime.title))
