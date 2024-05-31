import threading

from gi.repository import Gtk

from exceptions.mal_exceptions import (MalApiException,
                                       MalAuthorizationException)
from exceptions.ui_exceptions import UIException
from models.mal_model import MalAnimeUpdate
from pages.episode_page import EpisodePage
from services.jikan_service import JikanService
from services.mal_service import MalService, Status
from services.x_service import XService
from store.episode_store import EpisodeSotre
from store.mal_library_store import MalLibraryStore
from widgets.detail_header import DetailHeader
from widgets.dialogs import InfoDialog
from widgets.episodes_list_widget import EpisodesListWidget
from widgets.page import Page


class DetailPage(Page):
    def __init__(
        self,
        mal_id: int,
        header_bar: Gtk.HeaderBar,
        *args,
        **kwargs
    ):
        super().__init__(
            header_bar=header_bar,
            *args,
            **kwargs
        )
        self.event = threading.Event()
        self.mal_id = mal_id
        self.anime_info = None
        self.prev_status = None

        self.mal_id = mal_id

        self.mal_store = MalLibraryStore()
        self.mal_store.status = None
        self.episode_store = EpisodeSotre(mal_id=mal_id)

        self.jikan_service = JikanService()
        self.x_service = XService()
        self.mal_service = MalService()

        self.episode_widget = EpisodesListWidget(
            go_to=self.go_to,
            mal_store=self.mal_store,
            episode_store=self.episode_store,
            get_episode=self._get_episode,
        )
        self.detail_header = DetailHeader()

        self._init_ui()
        self._connect_signals()
        self._create_lib_option_dialog()
        self._start_workers()

    def on_destroy(self):
        self.header_bar.remove(child=self.box_in_headerbar)

    def on_load(self):
        self.header_bar.set_title_widget(self.box_in_headerbar)

    def set_episodes(self, *args, **kwargs):
        if not self.anime_info:
            return
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
        )
        self.stack.add_named(child=destination, name=EpisodePage.Meta.name)
        self.stack.set_visible_child(destination)

    def _init_ui(self):
        self.box = Gtk.Box()
        self.info_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.box_in_headerbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.settings_button = Gtk.Button(label="Settings")

        self.stack_for_switcher = Gtk.Stack()
        self.stack_for_switcher.props.transition_type = (
            Gtk.StackTransitionType.SLIDE_LEFT_RIGHT
        )
        self.stack_switcher = Gtk.StackSwitcher(
            stack=self.stack_for_switcher, margin_start=80, margin_end=80
        )

        self.box_in_headerbar.append(self.stack_switcher)
        self.box_in_headerbar.append(self.settings_button)

        self.header_bar.set_title_widget(self.box_in_headerbar)
        self.detail_header.strat_loading()

        self.stack_for_switcher.add_titled(
            child=self.info_page, name="info", title="Info"
        )
        self.stack_for_switcher.add_titled(
            child=self.episode_widget, name="episodes", title="Episodes"
        )
        self.add_child(self.stack_for_switcher)
        self.info_page.append(child=self.detail_header)

    def _connect_signals(self):
        self.episode_store.connect("value-changed", self.set_episodes)
        self.mal_store.connect("status-changed", self._status_changed)
        self.mal_store.connect("watched-episodes-changed", self._num_watched_changed)

        self.settings_button.connect("clicked", self.watch_or_settings)

    def _create_lib_option_dialog(self, *args, **kwargs):
        self.info_dialog = InfoDialog()
        self.info_dialog.connect("close-request", self._create_lib_option_dialog)

        self.info_dialog.watch.connect(
            "clicked",
            self._ubdate_status_clicked,
            Status.WATCHING,
        )
        self.info_dialog.plan_to_watch_button.connect(
            "clicked",
            self._ubdate_status_clicked,
            Status.PLAN_TO_WATCH,
        )
        self.info_dialog.completed_button.connect(
            "clicked",
            self._ubdate_status_clicked,
            Status.COMPLETED,
        )
        self.info_dialog.dropped_button.connect(
            "clicked",
            self._ubdate_status_clicked,
            Status.DROPPED,
        )
        if self.mal_store.status:
            self.info_dialog.update_status(status=self.mal_store.status)
        self.info_dialog.remove_button.connect("clicked", self._remove_from_lib)

    def _start_workers(self):
        threading.Thread(target=self._load_anime, daemon=True).start()
        threading.Thread(
            target=self._check_and_fetch_episodes_is_available, daemon=True
        ).start()
        threading.Thread(
            target=self._load_from_mal_if_user_is_login, daemon=True
        ).start()

    def _ubdate_status_clicked(self, _: Gtk.Button, status: Status):
        def do_update():
            self._update_mal_lib(payload=MalAnimeUpdate(status=self.mal_store.status))
            self._update_status_in_mal_store()

        self.mal_store.status = status
        threading.Thread(target=do_update, daemon=True).start()
        if status == Status.WATCHING:
            threading.Thread(target=self._load_episodes, daemon=True).start()

    def _remove_from_lib(self, _: Gtk.Button):
        def do_update():
            try:
                self.mal_service.delete_anime_from_lib(mal_id=self.mal_id)
                raise UIException("Anime Has been removed from your lib")
            except MalAuthorizationException:
                self.user_store.is_login = False
            except MalApiException as err:
                raise UIException(err.value)

        self.user_store.update_user_anime(
            prev_status=self.mal_store.status,
            mal_id=self.mal_id,
        )
        threading.Thread(target=do_update, daemon=True).start()
        self.mal_store.status = None

    def _status_changed(self, *args, **kwargs) -> None:
        """
        This run everytime where status was change
        """
        self.info_dialog.update_status(self.mal_store.status)

    def _num_watched_changed(self, *args, **kwargs):
        self.set_episodes()

        def do_update():
            try:
                self.mal_service.update_possition(
                    mal_id=self.mal_id,
                    payload=MalAnimeUpdate(num_watched_episodes=self.mal_store.num_watched_episodes)
                )

            except MalAuthorizationException:
                self.user_store.is_login = False
            except MalApiException as err:
                raise UIException(err.value)
        threading.Thread(target=do_update, daemon=True).start()

    def _update_status_in_mal_store(self):
        self.user_store.update_user_anime(
            mal_id=self.mal_id,
            prev_status=self.mal_store.prev_status,
            new_status=self.mal_store.status,
        )

    def _load_anime(self):
        """
        Load anime detail from jikan and display
        """
        data = self.jikan_service.get_by_id(self.mal_id)
        self.detail_header.set_data(anime=data)

        self.detail_header.end_loading()
        self.anime_info = data
        self.event.set()

    def _check_and_fetch_episodes_is_available(self):
        """
        Check is projectx has arleady fetched apisode and olso wait for and load anime
        """
        self.event.wait()
        self.episode_widget.start_loading()
        to_fetch = self.x_service.check(mal_id=self.mal_id)
        if to_fetch is True or self.mal_id in self.user_store.user_anime_ids.get(
            Status.WATCHING, {}
        ):
            self._load_episodes()
        else:
            self.episode_widget.end_loading()
            self.episode_widget.set_label()

    def _load_episodes(self):
        """
        If user add to watch or episode has been available
        fetch episodes in loop
        """
        self.info_dialog.update_status(self.mal_store.status)
        for episodes in self.x_service.fetch_eposodes(self.mal_id):
            if episodes is None:
                return
            self.episode_store.episodes = episodes

    def _load_from_mal_if_user_is_login(self):
        """
        If user is login get user info about current anime
        """
        if not self.user_store.is_login:
            return
        try:
            self.mal_store.mal_anime_info = self.mal_service.get_possition_by_mal_id(
                mal_id=self.mal_id
            )
        except MalAuthorizationException:
            self.user_store.is_login = False

    def _update_mal_lib(self, payload: MalAnimeUpdate):
        self.info_dialog.disable_all_buttons()
        try:
            self.mal_service.update_possition(mal_id=self.mal_id, payload=payload)

        except MalAuthorizationException:
            self.user_store.is_login = False
        except MalApiException as err:
            raise UIException(err.value)
        self.info_dialog.enalbe_all_buttons()
        self.info_dialog.update_status(status=self.mal_store.status)

    def _get_episode(self, episode: int):
        def episode_job(episode):
            data = self.x_service.fetch_episode(mal_id=self.mal_id, episode=episode)
            if not data:
                return
            episodes = self.episode_store.episodes
            episodes.append(data)
            self.episode_store.episodes = episodes

        threading.Thread(target=episode_job, daemon=True, args=(episode,)).start()

    class Meta:
        name = "detail"
