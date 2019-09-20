
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.boxes.models import BoxDonJuan
from cajas.concepts.models.concepts import Concept, ConceptType
from cajas.general_config.models.exchange import Exchange
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.movement.services.office_service import MovementOfficeManager
from cajas.office.models import OfficeCountry
from cajas.users.models import Partner
from cajas.webclient.views.get_ip import get_ip
from cajas.webclient.views.utils import get_object_or_none

from ..models.loan import Loan, LoanType
from ..models.loan_history import LoanHistory

movement_don_juan_manager = DonJuanManager()
movement_partner_manager = MovementPartnerManager()
movement_office_manager = MovementOfficeManager()
User = get_user_model()


class LoanPaymentManager(object):

    def add_payment(self, request):
        office = OfficeCountry.objects.get(pk=request.session['office'])
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        if request.data['history_type'] == LoanHistory.ABONO:
            self.create_payment(request)
            if loan.loan_type == LoanType.EMPLEADO:
                concept = get_object_or_404(Concept, name='Pago Abono préstamo empleado')
                data = {
                    'concept': concept,
                    'movement_type': 'IN',
                    'value': request.data['value'],
                    'detail': 'Pago abono {}'.format(loan),
                    'date': request.data['date'],
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                if loan.provider:
                    if loan.provider.code == 'DONJUAN':
                        data['box'] = BoxDonJuan.objects.get(office=office)
                        return movement_don_juan_manager.create_movement(data)
                    else:
                        data['partner'] = loan.provider
                        data['box'] = loan.provider.box
                        return movement_partner_manager.create_simple(data)
                else:
                    data['box_office'] = loan.office.box
                    return movement_office_manager.create_movement(data)
            elif loan.loan_type == LoanType.SOCIO_DIRECTO:
                concept = get_object_or_404(Concept, name='Pago Abono préstamo socio', concept_type=ConceptType.DOUBLE)
                user = loan.lender
                partner = Partner.objects.get(user=user, office=office)
                data = {
                    'partner': partner,
                    'box': partner.box,
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': request.data['value'],
                    'detail': 'Pago abono {}'.format(loan),
                    'date': request.data['date'],
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                return movement_partner_manager.create_double(data)
            else:
                concept = get_object_or_404(Concept, name='Pago Abono préstamo terceros')
                box_donjuan = get_object_or_404(BoxDonJuan, office=office)
                data = {
                    'box': box_donjuan,
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': request.data['value'],
                    'detail': 'Pago abono {}'.format(loan),
                    'date': request.data['date'],
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                return movement_don_juan_manager.create_movement(data)
        elif request.data['history_type'] == LoanHistory.INTEREST:
            self.interest_load_payment(request)
            if loan.loan_type == LoanType.EMPLEADO:
                concept = get_object_or_404(Concept, name='Pago Interés préstamo empleado')
                if loan.provider:
                    data = {
                        'partner': loan.provider,
                        'box': loan.provider.box,
                        'concept': concept,
                        'movement_type': 'IN',
                        'value': request.data['value'],
                        'detail': 'Pago abono {}'.format(loan),
                        'date': request.data['date'],
                        'responsible': request.user,
                        'ip': get_ip(request)
                    }
                    return movement_partner_manager.create_simple(data)
                else:
                    data = {
                        'box_office': loan.office.box,
                        'concept': concept,
                        'movement_type': 'IN',
                        'value': request.data['value'],
                        'detail': 'Pago abono {}'.format(loan),
                        'date': request.data['date'],
                        'responsible': request.user,
                        'ip': get_ip(request)
                    }
                    return movement_office_manager.create_movement(data)
            elif loan.loan_type == LoanType.SOCIO_DIRECTO:
                concept = get_object_or_404(Concept, name='Pago Interés Préstamo Socio Directo')
                user = loan.lender
                partner = Partner.objects.get(user=user, office=office)
                data = {
                    'partner': partner,
                    'box': partner.box,
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': request.data['value'],
                    'detail': 'Pago interés {}'.format(loan),
                    'date': request.data['date'],
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                return movement_partner_manager.create_double(data)
            else:
                concept = get_object_or_404(Concept, name='Pago Interés Préstamo')
                box_donjuan = get_object_or_404(BoxDonJuan, office=request.session['office'])
                data = {
                    'box': box_donjuan,
                    'concept': concept,
                    'movement_type': 'OUT',
                    'value': request.data['value'],
                    'detail': 'Pago interes {}'.format(loan),
                    'date': request.data['date'],
                    'responsible': request.user,
                    'ip': get_ip(request)
                }
                return movement_don_juan_manager.create_movement(data)

    def create_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        office = OfficeCountry.objects.get(pk=request.session['office'])
        exchange = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=datetime.now().month,
        )
        if loan.loan_type == LoanType.SOCIO_DIRECTO:
            new_balance_cop = loan.balance_cop - float(request.data['value_cop'])
            new_balance = new_balance_cop / exchange.exchange_cop_abono
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.ABONO,
                movement_type=LoanHistory.OUT,
                value=request.data['value'],
                value_cop=request.data['value_cop'],
                date=request.data['date'],
                balance_cop=new_balance_cop,
                balance=new_balance
            )
        else:
            new_balance = loan.balance - request.data['value']
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.ABONO,
                movement_type=LoanHistory.OUT,
                value=request.data['value'],
                value_cop=0,
                date=request.data['date'],
                balance_cop=0,
                balance=new_balance
            )

    def interest_load_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        LoanHistory.objects.create(
            loan=loan,
            history_type=LoanHistory.INTEREST,
            movement_type=LoanHistory.OUT,
            value=request.data['value'],
            value_cop=request.data['value_cop'],
            date=datetime.now(),
            balance=loan.balance,
            balance_cop=loan.balance_cop
        )

    def update_loan_history(self, loan, data):
        loan.value = data['value']
        loan.value_cop = data['value_cop']
        loan.date = data['date']
        loan.save()

    def update_all_payments_balance_partner_loan(self, payments, loan, exchange):
        balance_cop = 0
        for payment in payments:
            if payment.history_type == LoanHistory.LOAN:
                payment.balance_cop = balance_cop + payment.value_cop
                payment.balance = payment.balance_cop / exchange.exchange_cop_abono
                payment.save()
            elif payment.history_type == LoanHistory.ABONO:
                payment.balance_cop = balance_cop - payment.value_cop
                payment.balance = payment.balance_cop / exchange.exchange_cop_abono
                payment.save()
            else:
                payment.balance_cop = balance_cop
                payment.balance = payment.balance_cop / exchange.exchange_cop_abono
                payment.save()
            balance_cop = payment.balance_cop
        loan.balance_cop = balance_cop
        loan.balance = balance_cop / exchange.exchange_cop_abono
        loan.save()

    def update_all_payments_balance_employee_loan(self, payments, loan, exchange):
        balance = 0
        for payment in payments:
            if payment.history_type == LoanHistory.LOAN:
                payment.balance = balance + payment.value
                payment.balance_cop = 0
                payment.save()
            elif payment.history_type == LoanHistory.ABONO:
                payment.balance = balance - payment.value
                payment.balance_cop = 0
                payment.save()
            else:
                payment.balance = balance
                payment.balance_cop = 0
                payment.save()
            balance = payment.balance
        loan.balance = balance
        loan.balance_cop = 0
        loan.save()

    def update_loan_payment(self, data, office):
        loan_payment = LoanHistory.objects.get(pk=data['loan_pk'])
        loan = loan_payment.loan
        self.update_loan_history(loan_payment, data)
        all_payments = loan.related_payments.order_by('date', 'pk')
        exchange = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=datetime.now().month,
        )
        if loan.loan_type == LoanType.SOCIO_DIRECTO:
            self.update_all_payments_balance_partner_loan(all_payments, loan, exchange)
        else:
            self.update_all_payments_balance_employee_loan(all_payments, loan, exchange)
        print(all_payments)
