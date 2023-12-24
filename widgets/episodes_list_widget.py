from typing import List

from gi.repository import Gtk

from models.episodes_model import EpisodeElement


class EpisodesListWidget(Gtk.Box):
    def __init__(self, go_to, *args, **kwargs) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, hexpand=True)
        self.go_to = go_to

        self.spinner = Gtk.Spinner(hexpand=True, vexpand=True, visible=True)
        self.episode_not_found_label = Gtk.Label(
            label="""
                Episode not found, add to watch
            """,
            hexpand=True,
            vexpand=True,
            visible=False,
        )
        self.append(self.episode_not_found_label)
        self.append(self.spinner)
        self.scroll_view = Gtk.ScrolledWindow(vexpand=True, hexpand=True)

        self.flow_box = Gtk.FlowBox(
            column_spacing=20,
            row_spacing=20,
            max_children_per_line=50,
            margin_end=20,
            margin_start=20,
            margin_top=20,
            margin_bottom=20,
        )
        self.flow_box.set_column_spacing(20)

        self.flow_box.set_max_children_per_line(50)
        self.scroll_view.set_child()
        self.scroll_view.set_child(child=self.flow_box)

    def set_episodes(self, episodes: List[EpisodeElement]):
        self.append(self.scroll_view)
        self.flow_box.remove_all()
        sorted_episodes = sorted(episodes, key=lambda x: x.episode)
        for episode in sorted_episodes:
            button = Gtk.Button(
                label=str(episode.episode),
                css_classes=["card-button", "ctitle"],
                height_request=300,
                width_request=300,
            )
            button.connect("clicked", self.go_to, episode.episode)
            self.flow_box.append(child=button)

    def start_loading(self):
        self.spinner.set_visible(True)

    def end_loading(self):
        self.spinner.set_spinning(False)
        self.episode_not_found_label.set_visible(False)

        self.spinner.set_visible(False)

    def set_label(self):
        self.spinner.set_spinning(True)
        self.episode_not_found_label.set_visible(True)

    def remove_label(self):
        self.episode_not_found_label.set_visible(False)

    #
    def _go_to_episode(self, _: Gtk.Button, episode_number: int):
        destination = self.page(episode_number=episode_number, **self.to_inject)
        self.stack.add_named(child=destination, name=self.page.Meta.name)
        self.stack.set_visible_child(destination)
