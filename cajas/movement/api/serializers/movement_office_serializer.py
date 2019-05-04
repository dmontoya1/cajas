
from rest_framework import serializers

from cajas.movement.models.movement_office import MovementOffice


class MovementOfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementOffice
        fields = (
            'id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_office'
        )
