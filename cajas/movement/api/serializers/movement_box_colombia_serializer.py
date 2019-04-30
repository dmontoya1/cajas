
from rest_framework import serializers

from movement.models.movement_box_colombia import MovementBoxColombia


class MovementBoxColombiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementBoxColombia
        fields = (
            'id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_office'
        )
