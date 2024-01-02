from services.mal_service import Status
from widgets.base_lib import BaseMalLib


class CompletedPage(BaseMalLib):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = Status.COMPLETED
        self.load_animes()
        # self.user_store.connect("completed-update", self.load_animes)

    class Meta:
        name = "Completed"
