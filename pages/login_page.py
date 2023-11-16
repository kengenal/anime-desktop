import gi

gi.require_version('Gtk', '4.0')

from gi.repository import Gtk

from widgets.page import Page


class LoginPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        button = Gtk.Button(label="login")
        button.connect("clicked", self.login)
        button.set_halign(align=Gtk.Align.CENTER)
        button.set_valign(align=Gtk.Align.CENTER)
        button.set_hexpand(expand=True)
        button.set_vexpand(expand=True)
        self.append(button)

    def login(self, *args, **kwargs):
        self.user_store.is_login = True

    class Meta:
        name = "login"
