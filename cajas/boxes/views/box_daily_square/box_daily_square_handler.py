
from .box_daily_square_create import BoxCreate


class BoxDailySquareHandler(object):
    """
    """

    @classmethod
    def box_daily_square_create(cls, user):
        return BoxCreate(user).call()
