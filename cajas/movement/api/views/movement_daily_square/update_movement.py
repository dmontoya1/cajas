from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from webclient.views.get_ip import get_ip

from ....models.movement_daily_square import MovementDailySquare
from ....services.daily_square_service import MovementDailySquareManager
from ...serializers.movement_daily_square_serializer import MovementDailySquareSerializer

from api.CsrfExempt import CsrfExemptSessionAuthentication

import logging

logger = logging.getLogger(__name__)


class UpdateDailySquareMovement(generics.RetrieveUpdateAPIView):
    queryset = MovementDailySquare.objects.all()
    serializer_class = MovementDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        data = request.POST
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            daily_square_manager = MovementDailySquareManager()
            daily_square_manager.update_daily_square_movement(data)
            return Response(
                'Se ha actualizado el movimiento exitosamente',
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            logger.exception(str(e))
            return Response(
                'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                status=status.HTTP_204_NO_CONTENT
            )
