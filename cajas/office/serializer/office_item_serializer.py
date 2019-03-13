
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

from office.models.officeItems import OfficeItems


class OfficeItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeItems
        fields = ('office', 'name', 'description', 'price', 'brand', 'is_deleted', 'observations')

    def create(self, validated_data):
        item = OfficeItems.objects.create(**validated_data)
        return item
