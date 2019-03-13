
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from ..models.loan import Loan
from ..serializers.loan_payments import LoanPaymentSerializer
from ..services.loan_payment_service import loan_payment_manager


class LoanPaymentCreate(APIView):
    """
    """

    def post(self, request, format=None):
        serializer = LoanPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        loan = loan_payment_manager.add_payment(request)

        return Response(
            'Se ha añadido el abono exitosamente',
            status=status.HTTP_201_CREATED
        )
