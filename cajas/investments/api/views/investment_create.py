
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.investment_serializer import InvestmentSerializer
from ...services.investment_manager import InvestmentManager


class InvestmentCreate(APIView):

    def post(self, request, format=None):
        data = request.POST.copy()
        serializer = InvestmentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        investment_manager = InvestmentManager()
        investment_manager.investment_create(request)
        return Response(
            'Se ha creado la inversión exitosamente',
            status=status.HTTP_201_CREATED
        )
