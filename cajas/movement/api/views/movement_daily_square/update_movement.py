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
from ....services.daily_square_service import MovementDailySquareManager
from ...serializers.movement_daily_square_serializer import MovementDailySquareSerializer

from api.CsrfExempt import CsrfExemptSessionAuthentication


class UpdateDailySquareMovement(generics.RetrieveUpdateAPIView):
    queryset = MovementDailySquare.objects.all()
    serializer_class = MovementDailySquareSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        data = {}
        office_ = get_object_or_404(OfficeCountry, slug=request.POST['office_slug'])
        data['box_daily_square'] = BoxDailySquare.objects.get(user__pk=request.POST['user_id'], office=office_)
        data['concept'] = Concept.objects.get(pk=request.POST['concept'])
        data['date'] = request.POST['date']
        data['movement_type'] = request.POST['movement_type']
        data['value'] = request.POST['value']
        data['detail'] = request.POST['detail']
        data['ip'] = get_ip(request)
        data['unit'] = get_object_or_none(Unit, pk=request.POST.get('unit', None))
        data['user'] = get_object_or_none(User, pk=request.POST.get('user', None))
        data['office'] = get_object_or_none(OfficeCountry, pk=request.POST.get('office', None))

        data_mv = data.copy()
        update_mvment = MovementDailySquare.objects.filter(pk=self.kwargs['pk'])
        data_mv['movement'] = update_mvment.first()
        data_mv['box'] = data['box_daily_square']
        if data_mv['movement'].movement_type != data_mv['movement_type']:
            self.update_movement_type(data_mv)
        if data_mv['movement'].value != data_mv['value']:
            self.update_value(data_mv)
        if data_mv['user']:
            daily_square_manager = MovementDailySquareManager()
            total_movements = daily_square_manager.get_user_value(data_mv)
            stop = StopManager.validate_stop(data_mv)
            if stop == 0 or (stop >= (total_movements['value__sum'] + int(data_mv['value']))):
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

    def update_movement_type(self, data):
        update_mvment = data['movement']
        self.update_movement(data)
        if update_mvment.movement_don_juan:
            data['box'] = update_mvment.movement_don_juan.box_don_juan
            self.update_movement(data)
        if update_mvment.movement_don_juan_usd:
            data['box'] = update_mvment.movement_don_juan_usd.box_don_juan
            self.update_movement(data)
        if update_mvment.movement_partner:
            data['box'] = update_mvment.movement_partner.box_partner
            self.update_movement(data)
        if update_mvment.movement_office:
            data['box'] = update_mvment.movement_office.box_office
            self.update_movement(data)
        if update_mvment.movement_cd:
            data['box'] = update_mvment.movement_cd.box_daily_square
            self.update_movement(data)

    def update_value(self, data):
        update_mvment = data['movement']
        self.update_extern_value(data)
        if update_mvment.movement_don_juan:
            data['box'] = update_mvment.movement_don_juan.box_don_juan
            self.update_extern_value(data)
            update_mvment.movement_don_juan.value = data['value']
            update_mvment.movement_don_juan.save()
        if update_mvment.movement_don_juan_usd:
            data['box'] = update_mvment.movement_don_juan_usd.box_don_juan
            self.update_extern_value(data)
            update_mvment.movement_don_juan_usd.value = data['value']
            update_mvment.movement_don_juan_usd.save()
        if update_mvment.movement_partner:
            data['box'] = update_mvment.movement_partner.box_partner
            self.update_extern_value(data)
            update_mvment.movement_partner.value = data['value']
            update_mvment.movement_partner.save()
        if update_mvment.movement_office:
            data['box'] = update_mvment.movement_office.box_office
            self.update_extern_value(data)
            update_mvment.movement_office.value = data['value']
            update_mvment.movement_office.save()
        if update_mvment.movement_cd:
            data['box'] = update_mvment.movement_cd.box_daily_square
            self.update_extern_value(data)
            update_mvment.movement_cd.value = data['value']
            update_mvment.movement_cd.save()

    def update_movement(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance = box.balance + (int(data['movement'].value) * 2)
        else:
            box.balance = box.balance - (int(data['movement'].value) * 2)
        box.save()

    def update_extern_value(self, data):
        box = data['box']
        if data['movement_type'] == 'IN':
            box.balance -= int(data['movement'].value)
            box.balance += int(data['value'])
        else:
            box.balance += int(data['movement'].value)
            box.balance -= int(data['value'])
        box.save()
