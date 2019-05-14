
from rest_framework.generics import RetrieveAPIView

from ..serializers.loan_serializer import LoanSerializer
from ...models import Loan


class LoanDetail(RetrieveAPIView):
    """
    """

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
