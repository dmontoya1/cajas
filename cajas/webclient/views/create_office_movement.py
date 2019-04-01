import copy

from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from cajas.users.models.employee import Employee
from concepts.models.concepts import Concept
from cajas.core.services.email_service import EmailManager
from inventory.models.category import Category
from inventory.models.brand import Brand
from movement.models.movement_office import MovementOffice
from office.models.office import Office
from office.services.office_item_create import OfficeItemsManager

from .get_ip import get_ip

email_manager = EmailManager()
office_items_manager = OfficeItemsManager()


class CreateOfficeMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']
        ip = get_ip(request)

        movement = MovementOffice.objects.create(
            box_office=office.box,
            concept=concept,
            date=date,
            movement_type=movement_type,
            value=value,
            detail=detail,
            responsible=request.user,
            ip=ip,
        )
        if "destine_office" in request.POST:
            destine_office = Office.objects.get(pk=request.POST['destine_office'])
            if movement_type == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            movement1 = MovementOffice.objects.create(
                box_office=destine_office.box,
                concept=concept.counterpart,
                date=date,
                movement_type=contrapart,
                value=value,
                detail=detail,
                responsible=request.user,
                ip=ip,
            )
            secretary = Employee.objects.filter(office=office, charge__name='Secretaria').first()
            email_manager.send_office_mail(request, secretary.user.email)

        if "brand" in request.POST:
            aux = copy.deepcopy(request.POST)
            office = get_object_or_404(Office, slug=self.kwargs['slug'])
            brand = get_object_or_404(Brand, pk=request.POST["brand"])
            category = get_object_or_404(Category, pk=request.POST["category"])

            aux["office"] = office
            aux["brand"] = brand
            aux["category"] = category
            office_item = office_items_manager.create_office_item(aux)

        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:office', kwargs={'slug': office.slug}))
