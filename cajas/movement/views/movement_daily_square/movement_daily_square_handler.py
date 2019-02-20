
from .movement_create import MovementCreate


class MovementDailySquareHandler(object):
    """
    """

    @staticmethod
    def create_movement(data):
        return MovementCreate(data).call()
