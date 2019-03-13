
from rest_framework import serializers

from inventory.models.category import Category


class CateogrySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Category
        fields = ('id', 'name', 'is_active')
