
from rest_framework import serializers

from ...models.movement_daily_square_request_item import MovementDailySquareRequestItem
from cajas.inventory.api.serializer.brand_serializer import BrandSerializer


class MovementDailySquareRequestItemSerializer(serializers.ModelSerializer):
    """
    """

    brand = BrandSerializer(many=False, read_only=True)

    class Meta:
        model = MovementDailySquareRequestItem
        fields = ('movement', 'name', 'description', 'price', 'brand')
