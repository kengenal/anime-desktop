import gi
from gi.repository import Gtk

from widgets.page import Page


class SettingsPage(Page):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        button = Gtk.Button(label="Logout")
        button.set_halign(align=Gtk.Align.CENTER)
        button.set_valign(align=Gtk.Align.CENTER)
        button.connect("clicked", self.logout)
        button.set_hexpand(expand=True)
        button.set_vexpand(expand=True)
        self.append(button)

    def logout(self, *args, **kwargs):
        self.user_store.is_login = False

    class Meta:
        name = "settings"
