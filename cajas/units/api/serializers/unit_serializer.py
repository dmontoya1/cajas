
from rest_framework import serializers

from cajas.users.api.serializers.partner_serializer import PartnerSerializer
from ...models.units import Unit
from .unit_items_serializer import UnitItemSerializer
from cajas.users.api.serializers.user_serializer import UserSerializer


class UnitSerializer(serializers.ModelSerializer):
    """
    """

    collector = UserSerializer(many=False, read_only=True)
    partner = PartnerSerializer(many=False, read_only=True)
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
