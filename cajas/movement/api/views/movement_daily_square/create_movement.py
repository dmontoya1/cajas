
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from boxes.models.box_daily_square import BoxDailySquare
from boxes.models.box_don_juan import BoxDonJuan
from boxes.models.box_don_juan_usd import BoxDonJuanUSD
from inventory.models.brand import Brand
from cajas.users.models.user import User
from chains.models.chain import Chain
from concepts.models.concepts import Concept
from concepts.services.stop_service import StopManager
from general_config.models.country import Country
from loans.models.loan import Loan
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit
from webclient.views.get_ip import get_ip
from webclient.views.utils import get_object_or_none

from ....services.daily_square_service import MovementDailySquareManager
from ....models.movement_don_juan_usd import MovementDonJuanUsd
from ....models.movement_don_juan import MovementDonJuan
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem

class CreateDailySquareMovement(APIView):
    """
    """

    def post(self, request, format=None):
        daily_square_manager = MovementDailySquareManager()
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
        office = get_object_or_none(OfficeCountry, pk=request.POST.get('office', None))
        loan = get_object_or_none(Loan, pk=request.POST.get('loan', None))
        chain = get_object_or_none(Chain, pk=request.POST.get('chain', None))

        print("OFICNA", office)
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
            'office': office,
            'loan': loan,
            'chain': chain,
            '_user': user,
        }

        if concept.name == 'Compra Dólares':
            movement_djd = MovementDonJuanUsd.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuanUSD, office=office_),
                concept=concept,
                movement_type=request.POST['movement_type'],
                value=request.POST['buy_usd_value'],
                detail=request.POST['detail'],
                date=request.POST['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            if request.POST['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            movement_dj = MovementDonJuan.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuan, office=office_),
                concept=concept.counterpart,
                movement_type=contrapart,
                value=request.POST['buy_value'],
                detail=request.POST['detail'],
                date=request.POST['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            data['value'] = request.POST['buy_value']
            data['movement_type'] = 'OUT'
            movement = daily_square_manager.create_movement(data)
            movement.movement_don_juan = movement_dj
            movement.movement_don_juan_usd = movement_djd
            movement.save()

        elif concept.name == 'Venta Dólares':
            movement_djd = MovementDonJuanUsd.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuanUSD, office=office_),
                concept=concept,
                movement_type=request.POST['movement_type'],
                value=request.POST['sell_usd_value'],
                detail=request.POST['detail'],
                date=request.POST['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            if request.POST['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            movement_dj = MovementDonJuan.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuan, office=office_),
                concept=concept.counterpart,
                movement_type=contrapart,
                value=request.POST['sell_value'],
                detail=request.POST['detail'],
                date=request.POST['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            data['value'] = request.POST['sell_value']
            data['movement_type'] = 'IN'
            movement = daily_square_manager.create_movement(data)
            movement.movement_don_juan = movement_dj
            movement.movement_don_juan_usd = movement_djd
            movement.save()

        elif concept.name == "Entrega de Efectivo a CD":
            dq_target = get_object_or_404(User, pk=request.POST['dq'])
            box_daily_square_target = BoxDailySquare.objects.get(user=dq_target, office=office_)
            movement = daily_square_manager.create_movement(data)
            data['box'] = box_daily_square_target
            data['concept'] = concept.counterpart
            if movement_type == 'OUT':
                data['movement_type'] = 'IN'
            else:
                data['movement_type'] = 'OUT'
            movement_cd = daily_square_manager.create_movement(data)
            movement.movement_cd = movement_cd
            movement.save()
        else:
            if user:
                total_movements = daily_square_manager.get_user_value(data)
                stop_manager = StopManager()
                stop = stop_manager.validate_stop(data)
                if stop == 0 or (stop >= (total_movements['value__sum'] + int(data['value']))):
                    movement = daily_square_manager.create_movement(data)
                else:
                    return Response(
                        'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                        status=status.HTTP_204_NO_CONTENT
                    )
            else:
                if concept.name == "Compra de Inventario Unidad":
                    movement = daily_square_manager.create_movement(data)
                    print("movement", movement.office)
                    print("movement", movement.unit)
                    values = request.data["elemts"].split(",")
                    for value in values:
                        if request.data["form[form]["+value+"][name]"] == '' or request.data["form[form]["+value+"][price]"] == '':
                            MovementDailySquareRequestItem.objects.create(
                                movement=movement,
                            )
                        else:
                            if "form[form]["+value+"][is_replacement]" in request.data:
                                MovementDailySquareRequestItem.objects.create(
                                    movement=movement,
                                    name=request.data["form[form]["+value+"][name]"],
                                    brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                                    price=request.data["form[form]["+value+"][price]"],
                                    is_replacement=True
                                )
                            else:
                                MovementDailySquareRequestItem.objects.create(
                                    movement=movement,
                                    name=request.data["form[form]["+value+"][name]"],
                                    brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                                    price=request.data["form[form]["+value+"][price]"]
                                )
                else:
                    movement = daily_square_manager.create_movement(data)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
