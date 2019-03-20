
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from concepts.models.concepts import Concept
from boxes.models.box_don_juan import BoxDonJuan
from movement.services.don_juan_service import DonJuanManager
from office.models.office import Office

from .get_ip import get_ip

donjuan_manager = DonJuanManager()


class CreateDonJuanMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        office = get_object_or_404(Office, slug=self.kwargs['slug'])
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
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:box_don_juan', kwargs={'slug': office.slug}))
