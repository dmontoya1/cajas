
from concepts.models.concepts import Concept

from ...models.movement_don_juan import MovementDonJuan


class CreateMovementService(object):

    def __init__(self, box, concept, movement_type, value, detail, date, responsible, ip):
        self._box = box
        self._concept = concept
        self._movement_type = movement_type
        self._value = value
        self._detail = detail
        self._date = date
        self._responsible = responsible
        self._ip = ip

    def call(self):
        movement = MovementDonJuan(
            box_don_juan=self._box,
            concept=self._concept,
            movement_type=self._movement_type,
            value=self._value,
            detail=self._detail,
            date=self._date,
            responsible=self._responsible,
            ip=self._ip
        )
        movement.save()
        return movement
