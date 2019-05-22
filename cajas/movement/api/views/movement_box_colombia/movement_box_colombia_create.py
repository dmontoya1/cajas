
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.concepts.models.concepts import Concept
from cajas.core.services.email_service import EmailManager
from cajas.office.models.notifications import Notifications
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.employee import Employee
from cajas.webclient.views.get_ip import get_ip

from ....models.movement_box_colombia import MovementBoxColombia
from ....services.box_colombia_service import MovementBoxColombiaManager
from ...serializers.movement_box_colombia_serializer import MovementBoxColombiaSerializer
from ....services.movement_between_office_service import MovementBetweenOfficesManager


class MovementBoxColombiaCreate(generics.CreateAPIView):
    """
    """

    serializer_class = MovementBoxColombiaSerializer
    queryset = MovementBoxColombia.objects.all()

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        office = get_object_or_404(OfficeCountry, slug=self.kwargs['slug'])
        data['office'] = office
        data['ip'] = get_ip(request)
        data['responsible'] = request.user
        concept = get_object_or_404(Concept, pk=request.POST['concept'])

        movement_box_colombia_manager = MovementBoxColombiaManager()
        movement = movement_box_colombia_manager.create_box_colombia_movement(data)

        if "destine_office" in request.POST:
            destine_office = get_object_or_404(
                OfficeCountry, pk=data['destine_office']
            )
            data['destine_office'] = destine_office
            data['concept'] = concept
            movement_between_office_manager = MovementBetweenOfficesManager()
            movement_between_office_manager.create_between_offices_movement_request(data, movement.pk, 'BCO')
            secretary = Employee.objects.filter(office=destine_office.office, charge__name='Secretaria').first()
            if secretary:
                email_manager = EmailManager()
                email_manager.send_office_mail(request, secretary.user.email)
                Notifications.objects.create(
                    office=destine_office, office_sender=office,
                    concept=concept, detail=request.POST['detail'], value=request.POST['value']
                )

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
