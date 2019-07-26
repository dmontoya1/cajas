
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.loan_history_serializer import LoanHistorySerializer
from ...services.loan_payment_service import LoanPaymentManager


class LoanPaymentCreate(APIView):
    """
    """

    def post(self, request, format=None):
        serializer = LoanHistorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan_payment_manager = LoanPaymentManager()
        loan_payment_manager.add_payment(request)

        return Response(
            'Se ha añadido el pago exitosamente',
            status=status.HTTP_201_CREATED
        )
