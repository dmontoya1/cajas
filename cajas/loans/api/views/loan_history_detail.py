
from rest_framework.generics import RetrieveUpdateAPIView

from ..serializers.loan_history_serializer import LoanHistorySerializer
from ...models import LoanHistory


class LoanHistoryDetail(RetrieveUpdateAPIView):
    """
    """

    serializer_class = LoanHistorySerializer
    queryset = LoanHistory.objects.all()
