from const.mal import Status
from widgets.base_lib import BaseMalLib


class PlanToWatchPage(BaseMalLib):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = Status.PLAN_TO_WATCH
        self.load_animes()
        self.user_store.connect("plantowatch-update", self.load_animes)

    class Meta:
        name = "Plan to Watch"
