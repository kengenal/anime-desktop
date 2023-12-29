import threading
from enum import property
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from gi.repository import GObject, Gtk

from exceptions.mal_exceptions import MalLoginException
from services.mal_oath_service import MalOath2Service
from store.user_store import UserStore
from utils.secure_store import SecureStore
from widgets.page import Page


class Listener(GObject.Object):
    __gsignals__ = {
        "delivered-data": (GObject.SignalFlags.RUN_FIRST, None, (str, bool)),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._query_params = None

    @property
    def query_params(self):
        return self._query_params

    @query_params.setter
    def query_params(self, new_value):
        if new_value != self._query_params:
            self._query_params = new_value
            self.emit("delivered-data", "query_params", new_value)


class Handler(BaseHTTPRequestHandler):
    def __init__(self, listener: Listener, *args, **kwargs):
        self.listener = listener
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if "favicon" not in self.path:
            url_parser = urlparse(self.path)
            parse_query = parse_qs(url_parser.query)
            self.listener.query_params = parse_query
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello, world!")


class LoginPage(Page):
    def __init__(self, user_store: UserStore, *args, **kwargs):
        super().__init__(user_store=user_store, *args, **kwargs)
        self.secure_store = SecureStore()
        self.user_store = user_store
        self.box = Gtk.Box()
        self.mal_services = MalOath2Service()
        self.listener = Listener()
        self.listener.connect("delivered-data", self.end_login_process)
        handler = partial(Handler, self.listener)
        self.httpd = HTTPServer(("localhost", 3000), handler)

        self.button = Gtk.Button(
            vexpand=True,
            hexpand=True,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
        )

        self.spinner = Gtk.Spinner(visible=False)
        self.box_label = Gtk.Label(label="Login via MAL")
        self.button_box = Gtk.Box()
        self.button.connect("clicked", self.start_login)

        self.box.append(self.button)
        self.button_box.append(self.box_label)
        self.button_box.append(self.spinner)

        self.button.set_child(self.button_box)
        self.add_child(self.box)
        self.thred_worker = threading.Thread(target=self.do_start_login)
        self.thred_worker.daemon = True

    def start_login(self, _: Gtk.Button):
        self.disable_button()
        self.mal_services.authorize()
        self.thred_worker.start()

    def do_start_login(self):
        self.httpd.serve_forever()

    def stop_server(self):
        self.httpd.shutdown()

    def end_login_process(self, *args, **kwargs):
        try:
            access_token, refresh_token = self.mal_services.fetch_token(
                code=self.listener.query_params.get("code")
            )
            self.secure_store.set("token", access_token)
            self.secure_store.set("refresh_token", refresh_token)
            self.user_store.is_login = True
        except MalLoginException as err:
            print(err)
        self.enable_button()
        self.stop_server()

    def disable_button(self):
        self.button.set_sensitive(False)
        self.spinner.set_visible(True)
        self.spinner.set_spinning(True)
        self.box_label.set_visible(False)

    def enable_button(self):
        self.button.set_sensitive(True)
        self.spinner.set_visible(False)
        self.spinner.set_spinning(False)
        self.box_label.set_visible(True)

    class Meta:
        name = "login"
