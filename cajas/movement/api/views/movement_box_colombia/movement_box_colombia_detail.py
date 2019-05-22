
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.webclient.views.get_ip import get_ip

from ....models.movement_box_colombia import MovementBoxColombia
from ....services.box_colombia_service import MovementBoxColombiaManager
from ...serializers.movement_box_colombia_serializer import MovementBoxColombiaSerializer

logger = logging.getLogger(__name__)


class MovementBoxColombiaDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """

    serializer_class = MovementBoxColombiaSerializer
    queryset = MovementBoxColombia.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            box_colombia_manager = MovementBoxColombiaManager()
            box_colombia_manager.update_office_movement(data)
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
