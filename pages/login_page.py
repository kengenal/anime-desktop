from collections.abc import Callable, Iterable, Mapping
from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import TCPServer
from urllib.parse import urlparse, parse_qs
import gi
import threading

gi.require_version("Gtk", "4.0")

from gi.repository import Gtk, Gio, Adw, GLib, GObject

from widgets.page import Page


class Listener(GObject.Object):
    __gsignals__ = {
        "delivered-data": (GObject.SignalFlags.RUN_FIRST, None, (str, bool))
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
    def __init__(self, application: Adw.Application, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = Gio.SimpleAction(name="open_url")
        self.listener = Listener()
        self.listener.connect("delivered-data", self.end_login_process)
        handler = partial(Handler, self.listener)
        self.httpd = HTTPServer(("localhost", 8080), handler)

        button = Gtk.Button(label="login")
        button.connect("clicked", self.login)
        button.set_halign(align=Gtk.Align.CENTER)
        button.set_valign(align=Gtk.Align.CENTER)
        button.set_hexpand(expand=True)

        button2 = Gtk.Button(label="Stop")
        button2.connect("clicked", self.stop_server)
        button2.set_halign(align=Gtk.Align.CENTER)
        button2.set_valign(align=Gtk.Align.CENTER)
        button2.set_hexpand(expand=True)

        self.th = threading.Thread(target=self.do_start_login)
        self.th.daemon = True
        button.set_vexpand(expand=True)
        self.append(button)
        self.append(button2)

    def login(self, *args, **kwargs):
        self.th.start()

    def do_start_login(self):
        self.httpd.serve_forever()

    def stop_server(self, *args, **kwargs):
        self.httpd.shutdown()

    def end_login_process(self, *args, **kwargs):
        print(args, kwargs)

    class Meta:
        name = "login"
