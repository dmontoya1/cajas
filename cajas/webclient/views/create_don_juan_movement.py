
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

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
from cajas.movement.services.movement_between_office_service import MovementBetweenOfficesManager
from cajas.office.models.notifications import Notifications
from cajas.office.models.officeCountry import OfficeCountry

from .get_ip import get_ip

donjuan_manager = DonJuanManager()
email_manager = EmailManager()


class CreateDonJuanMovement(View):
    """
    """

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
            data['destine_office'] = destine_office
            data['concept'] = concept
            data['office'] = office
            movement_between_office_manager = MovementBetweenOfficesManager()
            movement_between_office_manager.create_between_offices_movement_request(data)
            secretary = Employee.objects.filter(office=destine_office.office, charge__name='Secretaria').first()
            if secretary:
                email_manager.send_office_mail(request, secretary.user.email)
                Notifications.objects.create(
                    office=destine_office, office_sender=office,
                    concept=concept, detail=request.POST['detail'], value=request.POST['value']
                )
        if concept == transfer_concept:
            if data['movement_type'] == MovementOffice.IN:
                data['movement_type'] = MovementOffice.OUT
            else:
                data['movement_type'] = MovementOffice.IN
            if data['destine_box'] == 'CAJA_OFICINA':
                don_juan_manager = DonJuanManager()
                data['box'] = get_object_or_404(BoxDonJuan, office=data['office']),
                don_juan_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_DON_JUAN_USD':
                don_juan_usd_manager = DonJuanUSDManager()
                data['box'] = get_object_or_404(BoxDonJuanUSD, office=data['office']),
                don_juan_usd_manager.create_movement(data)
            elif data['destine_box'] == 'CAJA_COLOMBIA':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Colombia"),
                box_colombia_manager.create_colombia_movement(data)
            elif data['destine_box'] == 'CAJA_BANCO':
                box_colombia_manager = MovementBoxColombiaManager()
                data['box'] = get_object_or_404(BoxColombia, name="Caja Banco"),
                box_colombia_manager.create_bank_colombia_movement(data)
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:box_don_juan', kwargs={'slug': office.slug}))
