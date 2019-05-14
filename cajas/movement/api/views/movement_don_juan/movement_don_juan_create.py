
from django.contrib import messages
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status


from ....models.movement_don_juan import MovementDonJuan
from ...serializers.movement_don_juan_serializer import MovementDonJuanSerializer

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.users.models.employee import Employee
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.core.services.email_service import EmailManager
from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest
from cajas.movement.models.movement_office import MovementOffice
from cajas.movement.services.box_colombia_service import MovementBoxColombiaManager
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.don_juan_usd_service import DonJuanUSDManager
from cajas.office.models.notifications import Notifications
from cajas.office.models.officeCountry import OfficeCountry

from cajas.webclient.views.get_ip import get_ip

donjuan_manager = DonJuanManager()
email_manager = EmailManager()


class MovementDonJuanCreate(generics.CreateAPIView):
    """
    """

    serializer_class = MovementDonJuanSerializer
    queryset = MovementDonJuan.objects.all()

    def post(self, request, *args, **kwargs):
        office = get_object_or_404(OfficeCountry, slug=self.kwargs['slug'])
        box = get_object_or_404(BoxDonJuan, office=office)
        ip = get_ip(request)
        transfer_concept = get_object_or_404(
            Concept,
            name='Traslado entre cajas Colombia',
            concept_type=ConceptType.DOUBLE
        )
        concept = get_object_or_404(Concept, pk=request.POST['concept'])
        data = {
            'box': box,
            'concept': concept,
            'date': request.POST['date'],
            'movement_type': request.POST['movement_type'],
            'value': request.POST['value'],
            'detail': request.POST['detail'],
            'responsible': request.user,
            'ip': ip,
        }
        movement = donjuan_manager.create_movement(data)
        if "destine_office" in request.POST:
            destine_office = OfficeCountry.objects.get(pk=request.POST['destine_office'])
            if request.POST['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            mv = MovementBetweenOfficeRequest.objects.create(
                box_office=destine_office.box,
                observation=request.POST['detail'],
                detail=request.POST['detail'],
                concept=concept,
                movement_type=contrapart,
                date=request.POST['date'],
                value=request.POST['value'],
                responsible=request.user,
                ip=ip,
            )
            secretary = Employee.objects.filter(office=destine_office.office, charge__name='Secretaria').first()
            if secretary:
                email_manager.send_office_mail(request, secretary.user.email)
                Notifications.objects.create(
                    office=destine_office, office_sender=office,
                    concept=concept, detail=request.POST['detail'], value=request.POST['value']
                )
        if concept == transfer_concept:
            if request.data['movement_type'] == MovementOffice.IN:
                data['movement_type'] = MovementOffice.OUT
            else:
                data['movement_type'] = MovementOffice.IN
            if request.data['destine_box'] == 'CAJA_OFICINA':
                don_juan_manager = DonJuanManager()
                data['box'] = get_object_or_404(BoxDonJuan, office=request.data['office']),
                don_juan_manager.create_movement(data)
            elif request.data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=request.data['office']),
                don_juan_usd_manager.create_movement(data)
            elif request.data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Colombia"),
                box_colombia_manager.create_colombia_movement(data)
            elif request.data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Banco"),
                box_colombia_manager.create_bank_colombia_movement(data)

        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return Response(
            'Se ha añadido el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
