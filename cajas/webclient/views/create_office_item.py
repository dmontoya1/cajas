
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


class CreateOfficeItem(View):
    """
    """

    def post(self, request, *args, **kwargs):
        # create_daily_square_movement
        print("hello :D")
        pass