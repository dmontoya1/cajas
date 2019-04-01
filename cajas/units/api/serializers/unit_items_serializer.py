
from rest_framework import serializers

from inventory.api.serializer.brand_serializer import BrandSerializer
from ...models.unitItems import UnitItems


class UnitItemSerializer(serializers.ModelSerializer):
    """
    """

    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = UnitItems
        fields = ('id', 'name', 'description', 'price', 'brand', 'is_deleted', 'observations')
