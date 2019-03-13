
from rest_framework import serializers

from ..models.units import Unit


class UnitSerializer(serializers.ModelSerializer):
    """
    """

    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'partner', 'collector', 'supervisor', 'is_active', 'unit_price')

    def get_unit_price(self, obj):
        total = 0
        for item in obj.related_items.all():
            total += item.price
        return total
