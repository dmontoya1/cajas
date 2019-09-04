from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.inventory.models.brand import Brand
from cajas.users.models.user import User
from cajas.chains.models.chain import Chain
from cajas.concepts.models.concepts import Concept
from cajas.concepts.services.stop_service import StopManager
from cajas.core.services.email_service import EmailManager
from cajas.loans.models.loan import Loan
from cajas.loans.services.loan_service import LoanManager
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.users.models.employee import Employee
from cajas.webclient.views.get_ip import get_ip
from cajas.webclient.views.utils import get_object_or_none

from ....services.daily_square_service import MovementDailySquareManager
from ....models.movement_don_juan_usd import MovementDonJuanUsd
from ....models.movement_don_juan import MovementDonJuan
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem

email_manager = EmailManager()


class CreateDailySquareMovement(APIView):
    """
    """

    def post(self, request, format=None):
        request_data = request.data
        daily_square_manager = MovementDailySquareManager()
        office_ = get_object_or_404(OfficeCountry, slug=request.POST['office_slug'])
        box_daily_square = BoxDailySquare.objects.get(user__pk=request.POST['user_id'], office=office_)
        concept = Concept.objects.get(pk=request.POST['concept'])
        date = request.POST['date']
        movement_type = request.POST['movement_type']
        value = request.POST.get('value', 0)
        detail = request.POST['detail']

        ip = get_ip(request)
        unit = get_object_or_none(Unit, pk=request.POST.get('unit', None))
        user = get_object_or_none(User, pk=request.POST.get('user', None))
        office = get_object_or_none(OfficeCountry, pk=request.POST.get('office', None))
        loan = get_object_or_none(Loan, pk=request.POST.get('loan', None))
        chain = get_object_or_none(Chain, pk=request.POST.get('chain', None))

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

        elif concept.name == "Traslado de Efectivo entre Cuadres Diarios":
            movement = daily_square_manager.create_movement(data)
            dq_target = get_object_or_404(User, pk=request.POST['dq'])
            box_daily_square_target = BoxDailySquare.objects.get(user=dq_target, office=office_)
            data['box'] = box_daily_square_target
            data['concept'] = concept.counterpart
            if movement_type == 'OUT':
                data['movement_type'] = 'IN'
            else:
                data['movement_type'] = 'OUT'
            movement_cd = daily_square_manager.create_movement(data)
            movement.movement_cd = movement_cd
            movement.user = dq_target
            movement.save()
            email_manager.send_cd_transfer_email(
                request,
                movement.box_daily_square.user.get_full_name(),
                movement.value,
                dq_target.email
            )
        elif concept.name == "Préstamo Personal Empleado":
            loan_manager = LoanManager()
            if request.user.is_superuser or request.user.is_secretary():
                data_loan = {
                    'request': request,
                    'value': request_data['value'],
                    'value_cop': 0,
                    'interest': request_data['interest'],
                    'time': request_data['time'],
                    'exchange': request_data['exchange'],
                    'office': office_.pk,
                    'loan_type': 'EMP',
                    'lender': request_data['lender_employee'],
                    'box_from': request_data['box_from'],
                }
                if request_data['box_from'] == 'partner':
                    data_loan['provider'] = request_data['partner_provider']
                loan_manager.create_employee_loan(data_loan)
            data['lender'] = Employee.objects.get(pk=int(request_data['lender_employee']))
            movement = daily_square_manager.create_movement(data)
        elif concept.name == "Compra de Inventario Unidad":
            movement = daily_square_manager.create_movement(data)
            values = request.data["elemts"].split(",")
            for value in values:
                if request.data["form[form][" + value + "][name]"] == '' or \
                   request.data["form[form][" + value + "][price]"] == '':
                    MovementDailySquareRequestItem.objects.create(
                        movement=movement,
                    )
                else:
                    if "form[form][" + value + "][is_replacement]" in request.data:
                        MovementDailySquareRequestItem.objects.create(
                            movement=movement,
                            name=request.data["form[form][" + value + "][name]"],
                            brand=get_object_or_404(Brand, pk=request.data["form[form][" + value + "][brand]"]),
                            price=request.data["form[form][" + value + "][price]"],
                            is_replacement=True
                        )
                    else:
                        MovementDailySquareRequestItem.objects.create(
                            movement=movement,
                            name=request.data["form[form][" + value + "][name]"],
                            brand=get_object_or_404(Brand, pk=request.data["form[form][" + value + "][brand]"]),
                            price=request.data["form[form][" + value + "][price]"]
                        )
        elif concept.name == 'Pago Abono préstamo empleado':
            data['user'] = User.objects.get(pk=request.data['lender-user'])
            movement = daily_square_manager.create_movement(data)
        else:
            if user:
                total_movements = daily_square_manager.get_user_value(data)
                stop_manager = StopManager(user)
                stop = stop_manager.get_user_movements_top_value_by_concept(concept)
                informative_value = stop_manager.get_informative_user_top_value_movements_by_concept(concept)
                if informative_value != 0 and informative_value <= (total_movements['value__sum'] + int(data['value'])):
                    email_manager.send_informative_top_notification(user, concept)
                if stop == 0 or (stop >= (total_movements['value__sum'] + int(data['value']))):
                    movement = daily_square_manager.create_movement(data)
                else:
                    return Response(
                        'Se ha alcanzado el tope para este usuario para este concepto. No se ha creado el movimiento.',
                        status=status.HTTP_204_NO_CONTENT
                    )
            else:
                movement = daily_square_manager.create_movement(data)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
