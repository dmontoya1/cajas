
from rest_framework import serializers

from inventory.models.brand import Brand
from .category_serializer import CategorySerializer


class BrandSerializer(serializers.ModelSerializer):
    """
    """

    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Brand
        fields = ('id', 'name', 'category', 'is_active')
