
from .box_daily_square_create import BoxCreate


class BoxDailySquareHandler(object):
    """
    """

    @staticmethod
    def box_daily_square_create(user, office):
        return BoxCreate(user, office).call()
