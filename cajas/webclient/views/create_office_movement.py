
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from concepts.models.concepts import Concept
from movement.models.movement_office import MovementOffice
from office.models.office import Office

from .get_ip import get_ip


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
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:office', kwargs={'slug': office.slug}))
