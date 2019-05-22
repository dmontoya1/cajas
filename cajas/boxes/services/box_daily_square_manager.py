
from ..models.box_daily_square import BoxDailySquare


class BoxDailySquareManager(object):

    def create_box(self, data):
        box, created = BoxDailySquare.objects.get_or_create(
            user=data['user'],
            office=data['office']
        )
        return box
