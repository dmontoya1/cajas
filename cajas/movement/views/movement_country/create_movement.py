
from ...models.movement_country import MovementCountry


class CreateMovementCountry(object):

    def __init__(self, data):
        self._box = data['box']
        self._concept = data['concept']
        self._movement_type = data['movement_type']
        self._value = data['value']
        self._detail = data['detail']
        self._date = data['date']
        self._responsible = data['responsible']
        self._ip = data['ip']

    def call(self):
        movement = MovementCountry.objects.create(
            box_country=self._box,
            concept=self._concept,
            movement_type=self._movement_type,
            value=self._value,
            detail=self._detail,
            date=self._date,
            responsible=self._responsible,
            ip=self._ip
        )
        return movement
