
from ...models.movement_daily_square import MovementDailySquare


class MovementCreate(object):
    """
    """

    def __init__(self, data):
        self._box = data['box']
        self._concept = data['concept']
        self._movement_type = data['movement_type']
        self._value = data['value']
        self._detail = data['detail']
        self._date = data['date']
        self._responsible = data['responsible']
        self._ip = data['ip']
        self._unit = data['unit']
        self._user = data['user']
        self._country = data['country']
        self._loan = data['loan']
        self._chain = data['chain']
        self._office = data['office']

    def call(self):
        movement = MovementDailySquare(
            box_daily_square=self._box,
            concept=self._concept,
            movement_type=self._movement_type,
            value=self._value,
            detail=self._detail,
            date=self._date,
            responsible=self._responsible,
            ip=self._ip,
            unit=self._unit,
            user=self._user,
            country=self._country,
            office=self._office,
        )
        movement.save()
        return movement
