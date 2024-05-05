from gi.repository import Gtk

from models.jikan_model import Datum
from widgets.network_image import AsyncImage


class DetailHeader(Gtk.Box):
    def __init__(self) -> None:
        super().__init__()
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)
        self.spinner = Gtk.Spinner(vexpand=True, hexpand=True)
        self.vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            margin_end=20,
            margin_start=20,
            margin_bottom=20,
            margin_top=20,
        )

        self.scroll_view.set_child(self.vbox)
        self.append(self.spinner)

    def set_data(self, anime: Datum) -> None:
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        main_info = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        title = Gtk.Label(
            label=anime.title,
            justify=Gtk.Justification.CENTER,
            selectable=True,
            css_classes=["ctitle"],
            width_request=100,
            height_request=100,
        )
        description = Gtk.Label(
            selectable=True,
            wrap=True,
            label=anime.synopsis or "",
            hexpand=True,
            justify=Gtk.Justification.CENTER,
        )

        if (
            anime.images
            and anime.images.jpg
            and anime.images.jpg.large_image_url
        ):
            image = AsyncImage(
                anime.images.jpg.large_image_url,
                width_request=300,
                height_request=300,
            )

            header_box.append(image)
        main_info.append(title)
        main_info.append(description)
        header_box.append(main_info)
        self.vbox.append(header_box)
        self.append(self.scroll_view)

    def strat_loading(self):
        self.spinner.set_visible(True)
        self.spinner.set_spinning(True)

    def end_loading(self):
        self.spinner.set_visible(False)
        self.spinner.set_spinning(False)
