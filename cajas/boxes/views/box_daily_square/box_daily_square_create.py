
from ...models.box_daily_square import BoxDailySquare


class BoxCreate(object):
    """
    """

    def __init__(self, user):
        self._user = user

    def call(self):
        box, created = BoxDailySquare.objects.get_or_create(
            user=self._user
        )
        return box
