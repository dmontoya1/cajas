
from django.contrib import messages
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.boxes.models.box_colombia import BoxColombia
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.users.models.employee import Employee
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.core.services.email_service import EmailManager
from cajas.office.models.notifications import Notifications
from cajas.office.models.officeCountry import OfficeCountry

from ...serializers.movement_don_juan_serializer import MovementDonJuanSerializer
from ....models.movement_don_juan import MovementDonJuan
from ....models.movement_office import MovementOffice
from ....services.box_colombia_service import MovementBoxColombiaManager
from ....services.don_juan_service import DonJuanManager
from ....services.don_juan_usd_service import DonJuanUSDManager
from ....services.movement_between_office_service import MovementBetweenOfficesManager
from ....services.office_service import MovementOfficeManager

from cajas.webclient.views.get_ip import get_ip


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
        donjuan_manager = DonJuanManager()
        movement = donjuan_manager.create_movement(data)
        if "destine_office" in request.POST:
            destine_office = OfficeCountry.objects.get(pk=request.POST['destine_office'])
            data['destine_office'] = destine_office
            data['concept'] = concept
            data['office'] = office
            movement_between_office_manager = MovementBetweenOfficesManager()
            movement_between_office_manager.create_between_offices_movement_request(data, movement.pk, 'BDJ')
            secretary = Employee.objects.filter(office=destine_office.office, charge__name='Secretaria').first()
            if secretary:
                email_manager = EmailManager()
                email_manager.send_office_mail(request, secretary.user.email)
                Notifications.objects.create(
                    office=destine_office, office_sender=office,
                    concept=concept, detail=request.POST['detail'], value=request.POST['value']
                )
        if concept == transfer_concept:
            data['concept'] = concept.counterpart
            if request.data['movement_type'] == MovementOffice.IN:
                data['movement_type'] = MovementOffice.OUT
            else:
                data['movement_type'] = MovementOffice.IN
            if request.data['destine_box'] == 'CAJA_OFICINA':
                office_manager = MovementOfficeManager()
                data['box_office'] = office.box
                movement_office = office_manager.create_movement(data)
                movement.movement_office = movement_office.pk
            elif request.data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=office)
                movement_don_juan_usd = don_juan_usd_manager.create_movement(data)
                movement.movement_don_juan_usd = movement_don_juan_usd
            elif request.data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Colombia")
                movement_box_colombia = box_colombia_manager.create_movement_box_colombia(data)
                movement.movement_box_colombia = movement_box_colombia.pk
            elif request.data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Banco")
                movement_box_bank_colombia = box_colombia_manager.create_bank_colombia_movement(data)
                movement.movement_box_colombia = movement_box_bank_colombia
            movement.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return Response(
            'Se ha añadido el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
