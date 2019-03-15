
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ...services.chains_manager import ChainManager

chain_manager = ChainManager()


class ChainPay(APIView):
    """
    """

    def post(self, request, format=None):
        chain_manager.chain_manager(request.data)
        return Response(
            'Se ha creado la cadena exitosamente.',
            status=status.HTTP_201_CREATED
        )
