
from rest_framework import serializers

from ...models.movement_daily_square import MovementDailySquare


class MovementDailySquareSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = MovementDailySquare
        fields = ('__all__')
