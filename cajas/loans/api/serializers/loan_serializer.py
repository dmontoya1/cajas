
from rest_framework import serializers

from cajas.loans.models.loan import Loan


class LoanSerializer(serializers.ModelSerializer):
    """
    """

    loan_type = serializers.SerializerMethodField()

    class Meta:
        model = Loan
        fields = ('id', 'provider', 'lender', 'office', 'loan_type', 'value', 'value_cop', 'interest',
                  'time', 'balance', 'exchange', 'description')

    def get_loan_type(self, obj):
        return str(obj.loan_type)
