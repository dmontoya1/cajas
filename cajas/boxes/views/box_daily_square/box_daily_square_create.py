
from ...models.box_daily_square import BoxDailySquare


class BoxCreate(object):
    """
    """

    def __init__(self, user):
        self._user = user

    def call(self):
        if not BoxDailySquare.objects.filter(user=self._user):
            box = BoxDailySquare(
                user=self._user
            )
            box.save()
        else:
            box = BoxDailySquare.objects.get(user=self._user)
        return box
