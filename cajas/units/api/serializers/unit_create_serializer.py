
from rest_framework import serializers

from ...models.units import Unit
from .unit_items_serializer import UnitItemSerializer


class UnitCreateSerializer(serializers.ModelSerializer):
    """
    """

    related_items = UnitItemSerializer(many=True, read_only=True)
    unit_price = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'partner', 'collector', 'supervisor', 'is_active', 'unit_price', 'related_items')

    def get_unit_price(self, obj):
        total = 0
        for item in obj.related_items.all():
            total += item.price
        return total
