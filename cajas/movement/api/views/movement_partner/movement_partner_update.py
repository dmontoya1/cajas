
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.webclient.views.get_ip import get_ip

from ....models.movement_partner import MovementPartner
from ....services.partner_service import MovementPartnerManager
from ...serializers.movement_partner_serializer import MovementPartnerSerializer

logger = logging.getLogger(__name__)
partner_manager = MovementPartnerManager()


class MovementPartnerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    """

    serializer_class = MovementPartnerSerializer
    queryset = MovementPartner.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            partner_manager.update_partner_movement(data)
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

    def delete(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']

        partner_manager.delete_partner_movement(data)
        return Response(
            'Se ha eliminado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
