from gi.repository import GLib, Gtk

from pages.detail_page import DetailPage
from services.jikan_service import JikanService
from widgets.card_widget_search import CardSearchWidget
from widgets.page import Page


class SearchPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.has_next_page = True
        self.is_loading = False
        self.page = 1
        self.query = ""
        self.jikan_service = JikanService()
        self.search = Gtk.SearchEntry()
        self.search.connect("search-changed", self.on_search)
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

        self.scroll_window.connect("edge-reached", self.scroll_position)
        self.loader = Gtk.Spinner(spinning=True, visible=True)

        self.loader.set_size_request(20, 20)

        self.box.append(self.scroll_window)
        self.box.append(self.loader)

        self.add_child(child=self.box)

        self.on_load()

        GLib.idle_add(self.gat_data)

    def on_load(self):
        self.header_bar.pack_start(self.search)

    def on_destroy(self):
        self.header_bar.remove(self.search)

    def gat_data(self):
        self.is_loading = True
        self.loader_activate()
        data = self.jikan_service.fetch_data(page=self.page, query=self.query)
        if data:
            self.has_next_page = data.pagination.has_next_page
            self.page = data.pagination.current_page

            for anime in data.data:
                button = Gtk.Button(css_classes=["card-button"])

                button.set_child(CardSearchWidget(anime=anime))
                button.connect("clicked", self.go_to_detail, anime.mal_id)
                button.set_size_request(300, 300)
                self.flow_box.append(button)

        self.loader_deactivate()
        self.is_loading = False

    def scroll_position(
        self, _: Gtk.ScrolledWindow, position: Gtk.PositionType
    ):
        if (
            position == Gtk.PositionType.BOTTOM
            and self.has_next_page
            and not self.is_loading
        ):
            self.page += 1
            GLib.idle_add(self.gat_data)

    def loader_activate(self):
        self.loader.set_spinning(True)
        self.loader.set_visible(True)

    def go_to_detail(self, _: Gtk.Button, mal_id: int):
        destination = DetailPage(
            mal_id=mal_id,
            user_store=self.user_store,
            stack=self.stack,
            header_bar=self.header_bar,
        )
        self.stack.add_named(child=destination, name=DetailPage.Meta.name)
        self.stack.set_visible_child(destination)

    def loader_deactivate(self):
        self.loader.set_spinning(False)
        self.loader.set_visible(False)

    def on_search(self, text: Gtk.SearchEntry):
        if len(text.get_text()) % 3 == 0:
            self.flow_box.remove_all()
            self.query = text.get_text()
            GLib.idle_add(self.gat_data)

    class Meta:
        name = "search"
