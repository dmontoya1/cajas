
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response

from cajas.office.models.officeCountry import OfficeCountry

from ..serializers.loan_history_serializer import LoanHistorySerializer
from ...models import LoanHistory
from ...services.loan_payment_service import LoanPaymentManager


class LoanHistoryDetail(RetrieveUpdateAPIView):
    """
    """

    serializer_class = LoanHistorySerializer
    queryset = LoanHistory.objects.all()

    def update(self, request, *args, **kwargs):
        office = OfficeCountry.objects.get(pk=request.session['office'])
        loan_payment_manager = LoanPaymentManager()
        loan_payment_manager.update_loan_payment(request.data, office)
        return Response(
            'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
            status=status.HTTP_204_NO_CONTENT
        )
