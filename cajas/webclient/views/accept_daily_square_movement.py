
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from movement.models.movement_daily_square import MovementDailySquare
from movement.views.movement_daily_square.movement_daily_square_handler import MovementDailySquareHandler

from .get_ip import get_ip


class AcceptDailySquareMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        movement = get_object_or_404(MovementDailySquare, pk=request.POST['movement_id'])
        ip = get_ip(request)
        data = {
            'movement': movement,
            'responsible': request.user,
            'ip': ip,
        }
        movement = MovementDailySquareHandler.accept_movement(data)
        messages.add_message(
            request,
            messages.SUCCESS,
            'El movimiento ha sido aceptado, se ha generado el movimiento en la caja correspondiente'
        )
        return HttpResponseRedirect(reverse('webclient:daily_square_box', kwargs={'pk': request.POST['user_id']}))
