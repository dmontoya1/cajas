
from rest_framework import serializers

from inventory.models.brand import Brand


class BrandSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Brand
        fields = ('id', 'name', 'category', 'is_active')
