
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.webclient.views.get_ip import get_ip

from ....models.movement_office import MovementOffice
from ....services.office_service import MovementOfficeManager
from ...serializers.movement_office_serializer import MovementOfficeSerializer

logger = logging.getLogger(__name__)


class MovementOfficeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """

    serializer_class = MovementOfficeSerializer
    queryset = MovementOffice.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            office_manager = MovementOfficeManager()
            office_manager.update_office_movement(data)
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
