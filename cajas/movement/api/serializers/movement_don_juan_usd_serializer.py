
from rest_framework import serializers

from ...models.movement_don_juan_usd import MovementDonJuanUsd


class MovementDonJuanUSDSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = MovementDonJuanUsd
        fields = ('__all__')
