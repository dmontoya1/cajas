
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.employee import Employee
from concepts.models.concepts import Concept
from core.services.email_service import EmailManager
from movement.services.don_juan_service import DonJuanManager
from office.models.notifications import Notifications
from office.models.officeCountry import OfficeCountry
from movement.models.movement_between_office_request import MovementBetweenOfficeRequest

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
                    office=office, office_sender=destine_office,
                    concept=concept, detail=request.POST['detail'], value=request.POST['value']
                )

        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:box_don_juan', kwargs={'slug': office.slug}))
