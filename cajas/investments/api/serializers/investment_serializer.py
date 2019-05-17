
from rest_framework import serializers

from ...models.investment import Investment


class InvestmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Investment
        fields = ('__all__')
