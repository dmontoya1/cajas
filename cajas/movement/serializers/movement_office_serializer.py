
from rest_framework import serializers

from movement.models.movement_office import MovementOffice


class MovementOfficeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovementOffice
        fields = ('id', 'movement_type', 'concept', 'value', 'detail', 'date', 'responsible', 'ip', 'balance', 'box_office')

    def create(self, validated_data):
        obj = MovementOffice.objects.create(**validated_data)
        return obj
