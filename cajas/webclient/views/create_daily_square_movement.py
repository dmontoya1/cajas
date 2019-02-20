
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import View

from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.user import User
from concepts.models.concepts import Concept
from general_config.models.country import Country
from movement.views.movement_daily_square.movement_daily_square_handler import MovementDailySquareHandler
from office.models.office import Office
from units.models.units import Unit

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
        try:
            unit = get_object_or_404(Unit, pk=request.POST['unit'])
        except:
            unit = None
        try:
            user = get_object_or_404(User, pk=request.POST['user'])
        except:
            user = None
        try:
            country = get_object_or_404(Country, pk=request.POST['country'])
        except:
            country = None
        try:
            loan = request.POST['loan']
        except:
            loan = None
        try:
            chain = request.POST['chain']
        except:
            chain = None
        try:
            office = get_object_or_404(Office, pk=request.POST['office'])
        except:
            office = None

        data = {
            'box': box_daily_square,
            'concept': concept,
            'date': date,
            'movement_type': movement_type,
            'value': value,
            'detail': detail,
            'responsible': request.user,
            'ip': ip,
            'unit': unit,
            'user': user,
            'country': country,
            'office': office,
            'loan': loan,
            'chain': chain,
        }

        movement = MovementDailySquareHandler.create_movement(data)
        messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        return HttpResponseRedirect(reverse('webclient:daily_square_box', kwargs={'pk': request.POST['user_id']}))
