
from django.contrib import messages
from django.http import HttpResponseRedirect
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

    @staticmethod
    def get_object_or_none(self, Model, **kwargs):
        try:
            return Model.objects.get(kwargs)
        except Model.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.POST['user_id'])
        box_daily_square = BoxDailySquare.objects.get(user=user)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        ip = get_ip(request)
        unit = self.get_object_or_none(Unit, pk=request.POST['unit'])
        user = self.get_object_or_none(User, pk=request.POST['user'])
        country = self.get_object_or_none(Country, pk=request.POST['country'])
        office = self.get_object_or_none(Office, pk=request.POST['office'])
        loan = request.POST['loan']
        chain = request.POST['chain']

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
