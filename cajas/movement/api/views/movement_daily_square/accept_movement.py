
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.boxes.models import BoxDonJuan
from cajas.concepts.models.concepts import Concept, Relationship
from cajas.loans.models.loan import Loan, LoanType
from cajas.loans.models.loan_history import LoanHistory
from cajas.loans.services.loan_payment_service import LoanPaymentManager
from cajas.office.models.officeCountry import OfficeCountry
from cajas.office.services.office_item_create import OfficeItemsManager
from cajas.units.models.unitItems import UnitItems
from cajas.users.models.partner import Partner
from cajas.webclient.views.get_ip import get_ip
from cajas.webclient.views.utils import get_president_user

from ....models.movement_daily_square import MovementDailySquare
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem
from ....services.don_juan_service import DonJuanManager
from ....services.office_service import MovementOfficeManager
from ....services.partner_service import MovementPartnerManager

president = get_president_user()


class AcceptMovement(APIView):
    """
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def post(self, request, format=None):
        office = OfficeCountry.objects.get(pk=request.session['office'])
        withdraw_concept = get_object_or_404(Concept, name="Retiro de Socio")
        movement = get_object_or_404(MovementDailySquare, pk=request.data['movement_id'])
        user = movement.box_daily_square.user
        movement_partner_manager = MovementPartnerManager()
        don_juan_manager = DonJuanManager()
        movement_office_manager = MovementOfficeManager()
        if movement.concept == withdraw_concept:
            partner = Partner.objects.get(user=movement.user, office=office)
            data = {
                'box': partner.box,
                'partner': partner,
                'value': movement.value,
                'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                'date': movement.date,
                'responsible': request.user,
                'ip': get_ip(request)
            }
            movement_partner_manager.create_withdraw_movement(data)
        else:
            relationship = movement.concept.relationship
            if relationship == Relationship.UNIT:
                if movement.unit.partner.user == president:
                    data = {
                        'box': BoxDonJuan.objects.get(office=movement.box_daily_square.office),
                        'concept': movement.concept,
                        'movement_type': movement.movement_type,
                        'value': movement.value,
                        'detail': '{} (Cuadre Diario: {} {}) (Unidad: {})'.format(
                            movement.detail,
                            user.first_name,
                            user.last_name,
                            movement.unit
                        ),
                        'date': movement.date,
                        'responsible': request.user,
                        'ip': get_ip(request)
                    }
                    unit_movement = don_juan_manager.create_movement(data)
                    movement.movement_don_juan = unit_movement
                else:
                    data = {
                        'box': movement.unit.partner.box,
                        'concept': movement.concept,
                        'movement_type': movement.movement_type,
                        'value': movement.value,
                        'detail': '{} (Cuadre Diario: {} {}) (Unidad: {})'.format(
                            movement.detail,
                            user.first_name,
                            user.last_name,
                            movement.unit
                        ),
                        'date': movement.date,
                        'responsible': request.user,
                        'ip': get_ip(request)
                    }
                    unit_movement = movement_partner_manager.create_simple(data)
                    movement.movement_partner = unit_movement
            elif relationship == Relationship.PERSON:
                data = {
                    'box': movement.user.partner.get().box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                movement_person = movement_partner_manager.create_simple(data)
                movement.movement_partner = movement_person
            elif relationship == Relationship.OFFICE:
                data = {
                    'box_office': movement.office.box,
                    'concept': movement.concept,
                    'movement_type': movement.movement_type,
                    'value': movement.value,
                    'detail': '{} (Cuadre Diario: {})'.format(movement.detail, user),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                movement_office_manager = MovementOfficeManager()
                office_movement = movement_office_manager.create_movement(data)
                movement.movement_office = office_movement
        if movement.concept.name == "Compra de Inventario Unidad":
            movement_items = MovementDailySquareRequestItem.objects.filter(
                movement=movement
            )
            for item in movement_items:
                if not item.name or not item.price or not item.brand:
                    return Response(
                        'Debe crearse el inventario de la unidad para aprobar el movimiento',
                        status=status.HTTP_206_PARTIAL_CONTENT
                    )
                else:
                    item_create = UnitItems()
                    item_create.name = item.name
                    item_create.price = item.price
                    item_create.brand = item.brand
                    if item.movement.unit is not None:
                        item_create.unit = item.movement.unit
                    else:
                        item_create.office = item.movement.office
                    if item.is_replacement:
                        item_create.is_replacement = True
                    item_create.save()
            movement_items.delete()
        elif movement.concept.name == "Compra Inventario Oficina":
            movement_items = MovementDailySquareRequestItem.objects.filter(
                movement=movement
            ).first()
            data_items = {
                'office': office,
                'name': movement_items.name,
                'description': movement_items.description,
                'price': movement_items.price,
                'brand': movement_items.brand
            }
            office_items_manager = OfficeItemsManager()
            office_items_manager.create_office_item(data_items)
            movement_items.delete()
        elif movement.concept.name == 'Abono Préstamo Empleado':
            try:
                user = movement.user
                loan = Loan.objects.get(lender=user, loan_type=LoanType.EMPLEADO)
                data = {
                    'concept': movement.concept,
                    'movement_type': 'IN',
                    'value': movement.value,
                    'detail': 'Pago abono {}'.format(loan),
                    'date': movement.date,
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                if loan.provider:
                    if loan.provider.user == president:
                        data['box'] = BoxDonJuan.objects.get(office=office)
                        movement = don_juan_manager.create_movement(data)
                    else:
                        data['partner'] = loan.provider
                        data['box'] = loan.provider.box
                        movement = movement_partner_manager.create_simple(data)
                else:
                    data['box_office'] = loan.office.box
                    movement = movement_office_manager.create_movement(data)
                new_balance = loan.balance - movement.value
                LoanHistory.objects.create(
                    loan=loan,
                    history_type=LoanHistory.ABONO,
                    movement_type=LoanHistory.OUT,
                    value=movement.value,
                    value_cop=0,
                    date=movement.date,
                    balance_cop=0,
                    balance=new_balance
                )
                loan_history_manager = LoanPaymentManager()
                loan_history_manager.update_all_payments_balance_employee_loan(
                    loan.related_payments.order_by('date', 'pk'),
                    loan,
                )
            except Loan.DoesNotExist:
                return Response(
                    'No se pudo encontrar el préstamo para el usuario {}'.format(user.get_full_name()),
                    status=status.HTTP_400_BAD_REQUEST
                )
        movement.review = True
        movement.status = MovementDailySquare.APPROVED
        movement.save()

        return Response(
            'El movimiento se ha aprobado exitosamente. Se ha creado el movimiento en la caja correspondiente',
            status=status.HTTP_201_CREATED
        )
