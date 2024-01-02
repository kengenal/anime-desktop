import threading

from gi.repository import Gtk

from models.mal_model import Mal
from pages.detail_page import DetailPage
from services.mal_service import MalService
from widgets.card_lib_widget import CardLibWidget
from widgets.page import Page


class BaseMalLib(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = None
        self.mal_service = MalService()
        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, hexpand=True, vexpand=True
        )
        self.spinner = Gtk.Spinner(vexpand=True, hexpand=True)
        self.flow_box = Gtk.FlowBox(
            column_spacing=20,
            row_spacing=20,
            max_children_per_line=50,
            margin_end=20,
            margin_start=20,
            margin_top=20,
            margin_bottom=20,
        )

        self.scroll_window = Gtk.ScrolledWindow(
            hexpand=True,
            vexpand=True,
        )

        self.scroll_window.set_policy(
            Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC
        )
        self.scroll_window.set_child(self.flow_box)

        self.box.append(self.spinner)
        self.box.append(self.scroll_window)

        self.add_child(self.box)

    def load_animes(self):
        threading.Thread(target=self._load, daemon=True).start()

    def go_to_detail(self, button: Gtk.Button, mal_id: int):
        destination = DetailPage(
            mal_id=mal_id,
            user_store=self.user_store,
            stack=self.stack,
            header_bar=self.header_bar,
            db=self.db,
            database_connection=self.database_connection,
        )
        self.stack.add_named(child=destination, name=DetailPage.Meta.name)
        self.stack.set_visible_child(destination)
        self.stack.set_visible_child(destination)

    def _start_loading(self):
        self.spinner.set_visible(True)
        self.spinner.set_spinning(True)

    def _end_loading(self):
        self.spinner.set_visible(False)
        self.spinner.set_spinning(False)

    def _load(self):
        self._start_loading()
        user_anime_list: Mal = self.mal_service.user_anime(status=self.status)
        for anime in user_anime_list.data:
            button = Gtk.Button(css_classes=["card-button"])
            card = CardLibWidget(anime.node)
            button.set_child(child=card)
            button.connect("clicked", self.go_to_detail, anime.node.id)
            button.set_size_request(300, 300)
            self.flow_box.append(button)
        self._end_loading()
