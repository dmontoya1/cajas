
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.chain_serializer import ChainSerializer
from ...services.chains_manager import ChainManager

chain_manager = ChainManager()


class ChainCreate(APIView):
    """
    """

    def post(self, request, format=None):
        serializer = ChainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        chain_manager.chain_manager(request.data)
        return Response(
            'Se ha creado la cadena exitosamente.',
            status=status.HTTP_201_CREATED
        )
