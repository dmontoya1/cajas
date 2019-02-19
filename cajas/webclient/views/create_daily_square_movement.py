
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.user import User
from concepts.models.concepts import Concept
from movement.models.movement_daily_square import MovementDailySquare

from .get_ip import get_ip


class CreateDailySquareMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.POST['user_id'])
        box_daily_square = BoxDailySquare.objects.get(user=user)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        ip = get_ip(request)

        movement = MovementDailySquare(
            box_daily_square=box_daily_square,
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
        return HttpResponseRedirect(reverse('webclient:daily_square_box', kwargs={'pk': request.POST['user_id']}))
