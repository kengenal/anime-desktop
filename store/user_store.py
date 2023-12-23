from gi.repository import GObject


class UserStore(GObject.Object):
    __gsignals__ = {"value-changed": (GObject.SignalFlags.RUN_FIRST, None, (str, bool))}

    def __init__(self):
        super().__init__()
        self._is_login = False

    @property
    def is_login(self) -> bool:
        return self._is_login

    @is_login.setter
    def is_login(self, new_value):
        if new_value != self._is_login:
            self._is_login = new_value
            self.emit("value-changed", "is_login", new_value)
