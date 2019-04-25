
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from webclient.views.get_ip import get_ip

from ....models.movement_don_juan_usd import MovementDonJuanUsd
from ....services.don_juan_usd_service import DonJuanUSDManager
from ...serializers.movement_don_juan_usd_serializer import MovementDonJuanUSDSerializer

logger = logging.getLogger(__name__)


class MovementDonJuanUSDUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    """

    serializer_class = MovementDonJuanUSDSerializer
    queryset = MovementDonJuanUsd.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            office_manager = DonJuanUSDManager()
            office_manager.update_don_juan_movement(data)
            return Response(
                'Se ha actualizado el movimiento exitosamente',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception(str(e))
            print(e)
            return Response(
                'Ha ocurrido un error inesperado. Comunicate con el administrador',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
