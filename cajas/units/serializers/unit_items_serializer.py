
from rest_framework import serializers

from ..models.unitItems import UnitItems


class UnitItemSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = UnitItems
        fields = ('id', 'name', 'description', 'price', 'brand', 'is_deleted', 'observations')
