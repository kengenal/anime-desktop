from gi.repository import Gtk

from store.user_store import UserStore


class Page(Gtk.Stack):
    def __init__(
        self,
        stack: Gtk.Stack,
        header_bar: Gtk.HeaderBar,
        user_store: UserStore,
        *args,
        **kwargs
    ):
        super().__init__()

        self.stack = stack
        self.header_bar = header_bar
        self.user_store = user_store
        self.stack.connect("notify::visible-child", self._connect_on_load)

    def _connect_on_load(self, *args, **kwargs):
        if self.stack.get_visible_child_name() == self.Meta.name:
            self.on_load()
        else:
            self.on_destroy()

    def on_load(self):
        pass

    def on_destroy(self):
        pass

    class Meta:
        name = None
