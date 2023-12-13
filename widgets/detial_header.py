import gi

from models.jikan_model import Datum
from widgets.network_image import AsyncImage

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk


class DetalHeader(Gtk.Box):
    def __init__(self, anime: Datum) -> None:
        super().__init__()
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, 
            margin_end=20, 
            margin_start=20, 
            margin_bottom=20, 
            margin_top=20
        )
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        main_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        vbox.append(header_box)

        self.scroll_view.set_child(vbox)
        title = Gtk.Label(
            label=anime.title,
            justify=Gtk.Justification.CENTER,
            selectable=True,
            css_classes=["ctitle"],
            width_request=100,
            height_request=100
        )
        description = Gtk.Label(
            selectable=True,
            wrap=True,
            label=anime.synopsis or "",
            hexpand=True,
            justify=Gtk.Justification.CENTER,
        )

        if anime.images and anime.images.jpg and anime.images.jpg.large_image_url:
            image = AsyncImage(
                anime.images.jpg.large_image_url,
                width_request=300,
                height_request=300
            )
         
            header_box.append(image)
        main_info.append(title)
        main_info.append(description)
        header_box.append(main_info)
        self.append(self.scroll_view)
