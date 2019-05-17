
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.investment_serializer import InvestmentSerializer
from ...services.investment_manager import InvestmentManager

investment_manager = InvestmentManager()


class InvestmentCreate(APIView):

    def post(self, request, format=None):
        data = request.data
        serializer = InvestmentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            investment_manager.investment_create(data)
            return Response(
                'Se ha creado la inversión exitosamente',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                'Ha ocurrido un error al procesar la solicitud. {}'.format(e),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
