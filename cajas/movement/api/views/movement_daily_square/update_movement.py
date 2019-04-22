from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from boxes.models.box_daily_square import BoxDailySquare
from concepts.models.concepts import Concept
from cajas.users.models.user import User
from concepts.services.stop_service import StopManager
from general_config.models.country import Country
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit
from webclient.views.get_ip import get_ip
from webclient.views.utils import get_object_or_none

from ....models.movement_daily_square import MovementDailySquare
from ...serializers.movement_daily_square_serializer import MovementDailySquareSerializer

from api.CsrfExempt import CsrfExemptSessionAuthentication


class UpdateDailySquareMovement(generics.RetrieveUpdateAPIView):
    queryset = MovementDailySquare.objects.all()
    serializer_class = MovementDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        office_ = get_object_or_404(OfficeCountry, slug=request.POST['office_slug'])
        box_daily_square = BoxDailySquare.objects.get(user__pk=request.POST['user_id'], office=office_)
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

        data = {
            'box_daily_square': box_daily_square,
            'unit': unit,
            'user': user,
            'country': country,
            'office': office,
            'concept': concept,
            'movement_type': movement_type,
            'value': value,
            'detail': detail,
            'date': date,
            'responsible': request.user,
            'ip': ip,
        }
        update_mvment = MovementDailySquare.objects.filter(pk=self.kwargs['pk'])
        if update_mvment.first().movement_type != movement_type:
            box = box_daily_square
            if movement_type == 'IN':
                box.balance = box.balance + (int(update_mvment.first().value) * 2)
            else:
                box.balance = box.balance - (int(update_mvment.first().value) * 2)
            box.save()
        if user:
            total_movements = daily_square_manager.get_user_value(data)
            stop = StopManager.validate_stop(data)
            if stop == 0 or (stop >= (total_movements['value__sum'] + int(data['value']))):
                update_mvment.update(**data)
                return Response(
                    'Se ha creado el movimiento exitosamente',
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                    status=status.HTTP_204_NO_CONTENT
                )
        else:
            update_mvment.update(**data)
            return Response(
                'Se ha actualizado el movimiento exitosamente',
                status=status.HTTP_201_CREATED
            )
