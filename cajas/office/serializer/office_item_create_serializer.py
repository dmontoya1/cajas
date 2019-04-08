
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from office.models.officeItems import OfficeItems
from inventory.api.serializer.brand_serializer import BrandSerializer


class OfficeItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeItems
        fields = ('office', 'name', 'description', 'price', 'brand', 'is_deleted', 'observations')
