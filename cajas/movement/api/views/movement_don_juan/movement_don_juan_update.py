
import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.core.services.email_service import EmailManager
from cajas.movement.services.movement_between_office_service import MovementBetweenOfficesManager
from cajas.office.models import OfficeCountry, Notifications
from cajas.users.models.employee import Employee
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_don_juan import MovementDonJuan
from ....services.don_juan_service import DonJuanManager
from ...serializers.movement_don_juan_serializer import MovementDonJuanSerializer

logger = logging.getLogger(__name__)
don_juan_manager = DonJuanManager()


class MovementDonJuanUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    """

    serializer_class = MovementDonJuanSerializer
    queryset = MovementDonJuan.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.POST.copy()
        data['pk'] = self.kwargs['pk']
        data['ip'] = get_ip(request)

        try:
            movement = don_juan_manager.update_don_juan_movement(data)
            if "destine_office" in request.POST:
                destine_office = OfficeCountry.objects.get(pk=request.POST['destine_office'])
                data['destine_office'] = destine_office
                data['concept'] = movement.concept
                data['office'] = movement.box_don_juan.office
                data['responsible'] = request.user
                movement_between_office_manager = MovementBetweenOfficesManager()
                movement_between_office_manager.create_between_offices_movement_request(data, movement.pk, 'BDJ')
                secretary = Employee.objects.filter(office=destine_office.office, charge__name='Secretaria').first()
                if secretary:
                    email_manager = EmailManager()
                    email_manager.send_office_mail(request, secretary.user.email)
                    Notifications.objects.create(
                        office=destine_office, office_sender=movement.box_don_juan.office,
                        concept=movement.concept, detail=request.POST['detail'], value=request.POST['value']
                    )
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

        don_juan_manager.delete_don_juan_movement(data)
        return Response(
            'Se ha eliminado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
