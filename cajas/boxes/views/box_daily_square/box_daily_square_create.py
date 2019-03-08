
from ...models.box_daily_square import BoxDailySquare


class BoxCreate(object):
    """
    """

    def __init__(self, user, office):
        self._user = user
        self._office = office

    def call(self):
        box, created = BoxDailySquare.objects.get_or_create(
            user=self._user,
            office=self._office
        )
        return box
