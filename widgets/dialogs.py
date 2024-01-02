from typing import Optional

from gi.repository import Gtk

from services.mal_service import Status


class InfoDialog(Gtk.Dialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        button_width = 100
        button_height = 50
        self.box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
        )
        self.watch = Gtk.Button(
            label="Watch",
            hexpand=True,
            vexpand=True,
            width_request=button_width,
            height_request=button_height,
            margin_end=20,
            margin_top=20,
            margin_start=20,
            margin_bottom=20,
            name=Status.WATCHING,
        )

        self.plan_to_watch_button = Gtk.Button(
            label="Plan to watch",
            hexpand=True,
            vexpand=True,
            width_request=button_width,
            height_request=button_height,
            margin_end=20,
            margin_top=20,
            margin_start=20,
            margin_bottom=20,
            name=Status.PLAN_TO_WATCH,
        )

        self.completed_button = Gtk.Button(
            label="Completed",
            hexpand=True,
            vexpand=True,
            width_request=button_width,
            height_request=button_height,
            margin_end=20,
            margin_top=20,
            margin_start=20,
            margin_bottom=20,
            name=Status.COMPLETED,
        )
        self.dropped_button = Gtk.Button(
            label="Dropped",
            hexpand=True,
            vexpand=True,
            width_request=button_width,
            height_request=button_height,
            margin_end=20,
            margin_top=20,
            margin_start=20,
            margin_bottom=20,
            name=Status.DROPPED,
        )

        self.remove_button = Gtk.Button(
            label="Remove",
            hexpand=True,
            vexpand=True,
            width_request=button_width,
            height_request=button_height,
            margin_end=20,
            margin_top=20,
            margin_start=20,
            margin_bottom=20,
        )
        self.prev_status = None
        self.box.append(self.watch)
        self.box.append(self.completed_button)
        self.box.append(self.plan_to_watch_button)
        self.box.append(self.dropped_button)
        self.box.append(self.remove_button)
        self.set_child(child=self.box)

    def update_status(self, status: Status):
        if self.prev_status:
            if btn := self._get_widet_by_status(self.prev_status):
                btn.set_sensitive(True)

        if btn := self._get_widet_by_status(status):
            btn.set_sensitive(False)

        self.prev_status = status

    def _get_widet_by_status(self, status: Status) -> Optional[Gtk.Button]:
        buttons = [
            x for x in self.box.observe_children() if x.get_name() == status
        ]
        if buttons:
            return buttons[0]
        return None

    def disable_all_buttons(self):
        for x in self.box.observe_children():
            x.set_sensitive(False)

    def enalbe_all_buttons(self):
        for button in self.box.observe_children():
            button.set_sensitive(True)
