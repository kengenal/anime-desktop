from const.mal import Status
from widgets.base_lib import BaseMalLib


class WatchingPage(BaseMalLib):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = Status.WATCHING
        self.load_animes()
        self.user_store.connect("watch-update", self.load_animes)

    class Meta:
        name = "watching"
