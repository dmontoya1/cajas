
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
from .utils import get_object_or_none


class CreateDailySquareMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        office_pk = request.session['office']
        office_session = Office.objects.get(pk=office_pk)
        user = User.objects.get(pk=request.POST['user_id'])
        box_daily_square = BoxDailySquare.objects.get(user=user)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        ip = get_ip(request)
        request.POST.get('unit', '')
        unit = get_object_or_none(Unit, pk=request.POST.get('unit', None))
        user = get_object_or_none(User, pk=request.POST.get('user', None))
        country = get_object_or_none(Country, pk=request.POST.get('country', None))
        office = get_object_or_none(Office, pk=request.POST.get('office', None))
        loan = request.POST.get('loan', None)
        chain = request.POST.get('chain', None)

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
        return HttpResponseRedirect(reverse('webclient:daily_square_box', kwargs={'slug': office_session.slug, 'pk': request.POST['user_id']}))