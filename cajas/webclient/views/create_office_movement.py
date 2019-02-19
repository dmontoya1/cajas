
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import View

from boxes.models.box_office import BoxOffice
from concepts.models.concepts import Concept
from movement.models.movement_office import MovementOffice
from office.models.office import Office

from .get_ip import get_ip


class CreateOfficeMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        box_office = BoxOffice.objects.get(pk=request.user.employee.related_secretary_office.box.pk)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']
        ip = get_ip(request)

        movement = MovementOffice(
            box_office=box_office,
            concept=concept,
            date=date,
            movement_type=movement_type,
            value=value,
            detail=detail,
            responsible=request.user,
            ip=ip,

        )
        movement.save()
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect('/')
