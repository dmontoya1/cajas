
from rest_framework import serializers

from ...models.chain import Chain


class ChainSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = Chain
        fields = ('id', 'name', 'office', 'places', 'place_value', 'chain_type')
