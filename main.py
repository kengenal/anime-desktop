import sys
from typing import List

import gi

from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.settings_page import SettingsPage
from pages.watching_page import WatchingPage
from store.user_store import UserStore

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_store = UserStore()
        self.authorized_pages = [WatchingPage.Meta.name, SettingsPage.Meta.name]
        self.unauthorized_pages = [LoginPage.Meta.name]
        self.pages = [SearchPage.Meta.name] + self.unauthorized_pages + self.authorized_pages
        self.set_title(title="Anime App")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_child(child=vbox)

        self._generate_header_bar()

        self.flap = Adw.Flap()

        vbox.append(child=self.flap)

        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.connect("notify::visible-child", self.stack_signal)

        self.flap.set_content(content=self.stack)

        self.register_side_bar_page(SearchPage)
        self.register_side_bar_page(LoginPage)

        stack_sidebar = Gtk.StackSidebar()
        stack_sidebar.set_stack(stack=self.stack)
        self.flap.set_flap(flap=stack_sidebar)
        self.user_store.connect("value-changed", self.update)

    def on_flap_button_toggled(self, *args, **kwargs):
        self.flap.set_reveal_flap(not self.flap.get_reveal_flap())

    def stack_signal(self, *args, **kwargs):
        if self.stack.get_visible_child_name() in self.pages:
            self.back_button.set_visible(False)
        else:
            self.back_button.set_visible(True)

    def go_back(self, *args, **kwargs):
        page_to_remove = self.stack.get_pages()[-1]

        if page_to_remove.get_name() not in self.pages:
            destination: Gtk.StackPage = self.stack.get_pages()[-2]
            self.stack.set_visible_child(child=destination.get_child())
            self.stack.remove(page_to_remove.get_child())

    def update(self, *args, **kwargs):
        if not self.user_store.is_login:
            self.remove_pages_by_list(self.authorized_pages)
            self.register_side_bar_page(LoginPage)

        if self.user_store.is_login:
            self.remove_pages_by_list(self.unauthorized_pages)
            self.register_side_bar_page(WatchingPage)
            self.register_side_bar_page(SettingsPage)

    def remove_pages_by_list(self, li: List[str]):
        pages_to_remove = [
            page for page in self.stack.get_pages() if page.get_name() in li
        ]
        self.stack.set_visible_child_name("search")
        for page_to_remove in pages_to_remove:
            self.stack.remove(child=page_to_remove.get_child())

    def register_side_bar_page(self, page):
        page_object = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.stack.add_titled(child=page_object, name=page.Meta.name, title=page.Meta.name.capitalize())
        page_object.append(child=page(**self._inject()))

    def _generate_header_bar(self):
        self.hide_side_bar_button = Gtk.ToggleButton()
        self.hide_side_bar_button.set_icon_name(icon_name='sidebar-show-right-rtl-symbolic')
        self.hide_side_bar_button.connect('clicked', self.on_flap_button_toggled)

        self.back_button = Gtk.Button(label="<")
        self.back_button.connect("clicked", self.go_back)
        self.back_button.set_visible(True)

        self.header_bar = Gtk.HeaderBar()
        self.set_titlebar(titlebar=self.header_bar)
        self.header_bar.pack_start(child=self.hide_side_bar_button)
        self.header_bar.pack_start(child=self.back_button)

    def _inject(self):
        return {
            "stack": self.stack,
            "user_store": self.user_store,
            "header_bar": self.header_bar
        }


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.win = None

    def on_activate(self, app: Adw.Application):
        self.win = MainWindow(application=app)
        self.win.set_default_size(1070, 720)
        self.win.present()


app = MyApp(application_id="com.example.GtkApplication")
app.run(sys.argv)
