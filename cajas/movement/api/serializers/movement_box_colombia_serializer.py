
from rest_framework import serializers

from cajas.movement.models.movement_box_colombia import MovementBoxColombia


class MovementBoxColombiaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementBoxColombia
        fields = (
            'id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_office',
            'movement_don_juan', 'movement_office', 'movement_don_juan_usd', 'movement_box_colombia'
        )
