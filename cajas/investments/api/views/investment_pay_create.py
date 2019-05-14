
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.investment_pay_serializer import InvestmentPaySerializer
from ...services.investment_pay_manager import InvestmentPayManager

investment_pay_manager = InvestmentPayManager()


class InvestmentPayCreate(APIView):
    """
    """

    def post(self, request, format=None):
        serializer = InvestmentPaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pay = investment_pay_manager.add_payment(request)
        return Response(
            'Se ha añadido el abono exitosamente',
            status=status.HTTP_201_CREATED
        )
