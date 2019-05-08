
from rest_framework import serializers

from cajas.office.models.officeItems import OfficeItems
from cajas.inventory.api.serializer.brand_serializer import BrandSerializer


class OfficeItemSerializer(serializers.ModelSerializer):

    brand = BrandSerializer(read_only=True)

    class Meta:
        model = OfficeItems
        fields = ('office', 'name', 'description', 'price', 'brand', 'is_deleted', 'observations')
