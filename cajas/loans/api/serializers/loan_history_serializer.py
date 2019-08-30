
from rest_framework import serializers

from cajas.loans.models.loan_history import LoanHistory


class LoanHistorySerializer(serializers.ModelSerializer):
    """
    """

    class Meta:
        model = LoanHistory
        fields = ('id', 'history_type', 'movement_type', 'value', 'value_cop', 'date', 'balance', 'balance_cop')
