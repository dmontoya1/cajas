
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ...services.chains_manager import ChainManager


class UserPlaceUpdate(APIView):
    """
    """

    def post(self, request, format=None):
        chain_manager = ChainManager()
        chain_manager.user_place_update(request)
        return Response(
            'Se ha editado el puesto de la cadena exitosamente.',
            status=status.HTTP_201_CREATED
        )
