
from rest_framework import serializers

from ...models.investment_pay import InvestmentPay


class InvestmentPaySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvestmentPay
        fields = ('__all__')
