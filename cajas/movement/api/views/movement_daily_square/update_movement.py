
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare
from ....services.daily_square_service import MovementDailySquareManager
from ...serializers.movement_daily_square_serializer import MovementDailySquareSerializer

logger = logging.getLogger(__name__)
daily_square_manager = MovementDailySquareManager()


class UpdateDailySquareMovement(generics.RetrieveUpdateDestroyAPIView):
    queryset = MovementDailySquare.objects.all()
    serializer_class = MovementDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:

            daily_square_manager.update_daily_square_movement(data)
            return Response(
                'Se ha actualizado el movimiento exitosamente',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception(str(e))
            print(e)
            return Response(
                'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                status=status.HTTP_204_NO_CONTENT
            )

    def delete(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']

        daily_square_manager.delete_daily_square_movement(data)
        return Response(
            'Se ha actualizado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
