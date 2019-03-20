
from rest_framework import serializers

from ..models.loan_payments import LoanPayment


class LoanPaymentSerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = LoanPayment
        fields = ('id', 'value', 'date')
