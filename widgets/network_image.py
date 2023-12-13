import gi

from gi.repository import Gtk, GdkPixbuf, GLib, Gio


class AsyncImage(Gtk.Image):
    def __init__(self, url: str, *args, **kwargs):
        super().__init__( *args, **kwargs)
        file = Gio.file_new_for_uri(url)
    
        file.load_contents_async(None, self.on_load_complete)

    def on_load_complete(self, file: Gio.File, result: Gio.AsyncResult):
        is_loaded, stream, _ = file.load_contents_finish(result)
        if is_loaded:
            loader = GdkPixbuf.PixbufLoader()
            loader.write_bytes(GLib.Bytes.new(stream))
            loader.close()

            self.set_from_pixbuf(loader.get_pixbuf())
