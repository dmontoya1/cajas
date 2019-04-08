
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import View

from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.user import User
from concepts.models.concepts import Concept
from concepts.services.stop_service import StopManager
from general_config.models.country import Country
from movement.services.daily_square_service import MovementDailySquareManager
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit

from .get_ip import get_ip
from .utils import get_object_or_none

daily_square_manager = MovementDailySquareManager()


class CreateDailySquareMovement(View):
    """
    """

    def post(self, request, *args, **kwargs):
        office_pk = request.session['office']
        office_session = OfficeCountry.objects.get(pk=office_pk)
        user = User.objects.get(pk=request.POST['user_id'])
        box_daily_square = BoxDailySquare.objects.get(user=user)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST['value']
        detail = request.POST['detail']

        ip = get_ip(request)
        unit = get_object_or_none(Unit, pk=request.POST.get('unit', None))
        user = get_object_or_none(User, pk=request.POST.get('user', None))
        country = get_object_or_none(Country, pk=request.POST.get('country', None))
        office = get_object_or_none(OfficeCountry, pk=request.POST.get('office', None))
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

        total_movements = daily_square_manager.get_user_value(data)
        if StopManager.validate_stop(data) > total_movements['value__sum']:
            movement = daily_square_manager.create_movement(data)
            messages.add_message(request, messages.SUCCESS, 'Se ha añadido el movimiento exitosamente')
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.'
            )
        return HttpResponseRedirect(reverse('webclient:daily_square_box',
                                            kwargs={'slug': office_session.slug, 'pk': request.POST['user_id']}))
