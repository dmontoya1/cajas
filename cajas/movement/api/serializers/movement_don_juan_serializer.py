
from rest_framework import serializers

from ...models.movement_don_juan import MovementDonJuan


class MovementDonJuanSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = MovementDonJuan
        fields = ('__all__')
