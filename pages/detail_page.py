import threading
from sqlite3 import Connection, Cursor

from gi.repository import Gtk

from exceptions.mal_exceptions import MalAuthorizationException
from pages.episode_page import EpisodePage
from services.jikan_service import JikanService
from services.mal_service import MalService, Status
from services.x_service import XService
from store.episode_store import EpisodeSotre
from store.mal_library_store import MalLibraryStore
from widgets.detial_header import DetailHeader
from widgets.dialogs import InfoDialog
from widgets.episodes_list_widget import EpisodesListWidget
from widgets.page import Page


class DetailPage(Page):
    def __init__(
        self,
        mal_id: int,
        header_bar: Gtk.HeaderBar,
        db: Cursor,
        database_connection: Connection,
        *args,
        **kwargs
    ):
        super().__init__(
            header_bar=header_bar,
            db=db,
            database_connection=database_connection,
            *args,
            **kwargs
        )
        self.mal_id = mal_id
        self.event = threading.Event()
        self.mal_store = MalLibraryStore()
        self.database_connection = database_connection
        self.mal_id = mal_id
        self.anime_info = None

        self.jikan_service = JikanService()
        self.x_service = XService()
        self.mal_service = MalService()

        self.box = Gtk.Box()
        self.box_in_headerbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        self.stack_for_switcher = Gtk.Stack()
        self.stack_for_switcher.props.transition_type = (
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        )
        self.stack_switcher = Gtk.StackSwitcher(
            stack=self.stack_for_switcher, margin_start=80, margin_end=80
        )

        self.settings_button = Gtk.Button(label="Settings")

        self.settings_button.connect("clicked", self.watch_or_settings)

        self.box_in_headerbar.append(self.stack_switcher)
        self.box_in_headerbar.append(self.settings_button)

        header_bar.set_title_widget(self.box_in_headerbar)

        self.episode_store = EpisodeSotre(mal_id=mal_id)
        self.episode_store.connect("value-changed", self.set_episodes)

        self.episode_widget = EpisodesListWidget(
            go_to=self.go_to, mal_store=self.mal_store
        )

        self.detail_header = DetailHeader()
        self.detail_header.strat_loading()

        self.info_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.stack_for_switcher.add_titled(
            child=self.info_page, name="info", title="Info"
        )
        self.stack_for_switcher.add_titled(
            child=self.episode_widget, name="episodes", title="Episodes"
        )
        self.add_child(self.stack_for_switcher)
        self.mal_store.status = None
        self.info_page.append(child=self.detail_header)

        self._create_lib_option_dialog()

        self.mal_store.connect("status-changed", self._status_signal)
        self.mal_store.connect(
            "watched-episodes-changed", self._num_watched_episodes_signal
        )

        threading.Thread(target=self._load_anime, daemon=True).start()
        threading.Thread(
            target=self._check_and_fetch_episodes_is_available, daemon=True
        ).start()
        threading.Thread(
            target=self._load_from_mal_if_user_is_login, daemon=True
        ).start()

    def on_destroy(self):
        self.header_bar.remove(child=self.box_in_headerbar)

    def on_load(self):
        self.header_bar.set_title_widget(self.box_in_headerbar)

    def set_episodes(self, *args, **kwargs):
        self.episode_widget.remove_label()
        self.episode_widget.end_loading()
        self.episode_widget.set_episodes(
            episodes=self.anime_info.episodes,
            available_episodes=self.episode_store.episodes,
        )

    def watch_or_settings(self, *args, **kwargs):
        self.info_dialog.set_transient_for(self.get_native())
        self.info_dialog.present()

    def go_to(self, _: Gtk.Button, episode_number: int):
        if episode_number >= self.mal_store.num_watched_episodes:
            self.mal_store.num_watched_episodes = episode_number
        destination = EpisodePage(
            mal_store=self.mal_store,
            episode_number=episode_number,
            episode_store=self.episode_store,
            stack=self.stack,
            user_store=self.user_store,
            header_bar=self.header_bar,
            db=self.db,
            database_connection=self.database_connection,
        )
        self.stack.add_named(child=destination, name=EpisodePage.Meta.name)
        self.stack.set_visible_child(destination)

    def _update_user_library_anime_status(self, _: Gtk.Button, status: Status):
        self.mal_store.status = status
        if status == Status.WATCHING:
            threading.Thread(target=self._load_episodes, daemon=True).start()

    def _remove_from_lib(self, _: Gtk.Button):
        print("REMOVE")

    def _create_lib_option_dialog(self, *args, **kwargs):
        self.info_dialog = InfoDialog()
        self.info_dialog.connect(
            "close-request", self._create_lib_option_dialog
        )

        self.info_dialog.watch.connect(
            "clicked", self._update_user_library_anime_status, Status.WATCHING
        )
        self.info_dialog.plan_to_watch_button.connect(
            "clicked",
            self._update_user_library_anime_status,
            Status.PLAN_TO_WATCH,
        )
        self.info_dialog.completed_button.connect(
            "clicked", self._update_user_library_anime_status, Status.COMPLETED
        )
        self.info_dialog.dropped_button.connect(
            "clicked", self._update_user_library_anime_status, Status.DROPPED
        )

    def _status_signal(self, *args, **kwargs) -> None:
        self.info_dialog.update_status(self.mal_store.status)

    def _num_watched_episodes_signal(self, *args, **kwargs):
        print(self.mal_store.num_watched_episodes)

    def _load_anime(self):
        data = self.jikan_service.get_by_id(self.mal_id)
        self.detail_header.set_data(anime=data)

        self.detail_header.end_loading()
        self.anime_info = data
        self.event.set()

    def _check_and_fetch_episodes_is_available(self):
        self.event.wait()
        self.episode_widget.start_loading()
        to_fetch = self.x_service.check(mal_id=self.mal_id)
        if (
            to_fetch is True
            or self.mal_id in self.user_store.watching_anime_ids
        ):
            self._load_episodes()
        else:
            self.episode_widget.end_loading()
            self.episode_widget.set_label()

    def _load_episodes(self):
        self.info_dialog.update_status(Status.WATCHING)
        self.mal_store.status = Status.WATCHING
        for episodes in self.x_service.fetch_eposodes(self.mal_id):
            if episodes is None:
                return
            self.episode_store.episodes = episodes

    def _load_from_mal_if_user_is_login(self):
        if not self.user_store.is_login:
            return
        try:
            self.mal_store.mal_anime_info = (
                self.mal_service.get_possition_by_mal_id(mal_id=self.mal_id)
            )
        except MalAuthorizationException:
            self.user_store.is_login = False

    class Meta:
        name = "detail"
