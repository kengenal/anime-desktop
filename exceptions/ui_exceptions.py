from gi.repository import Gtk


class UIException(Exception):
    def __init__(self, message: str):
        self.alert = Gtk.MessageDialog(
            buttons=Gtk.ButtonsType.CLOSE,
            transient_for=Gtk.Window(),
            text=message,
        )
        self.alert.connect("response", self.close)
        self.alert.present()

    def close(self, *args, **kwargs):
        self.alert.destroy()
