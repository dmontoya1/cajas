
from rest_framework import serializers

from ..models.units import Unit


class UnitSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Unit
        fields = ('id', 'name', 'partner', 'collector', 'supervisor', 'is_active')
