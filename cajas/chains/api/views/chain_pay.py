
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ...services.chains_manager import ChainManager

chain_manager = ChainManager()


class ChainPay(APIView):
    """
    """

    def post(self, request, format=None):
        chain_manager.internal_chain_pay(request.data)
        return Response(
            'Se ha creado el pago exitosamente',
            status=status.HTTP_201_CREATED
        )
