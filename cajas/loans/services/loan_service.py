
from datetime import datetime

from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from concepts.models.concepts import Concept
from office.models.office import Office
from movement.views.movement_don_juan.movement_don_juan_handler import MovementDonJuanHandler
from movement.views.movement_partner.movement_partner_handler import MovementPartnerHandler
from webclient.views.get_ip import get_ip
from webclient.views.utils import get_object_or_none

from ..models.loan import Loan


User = get_user_model()


class LoanManager(object):

    PROPERTIES = ['value', 'value_cop', 'interest', 'time', 'exchange', 'office', 'loan_type']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_partner_loan(self, data):
        self.__validate_data(data)
        lender_partner = get_object_or_404(Partner, pk=data['lender'])
        lender = lender_partner.user
        old_loan = get_object_or_none(Loan, lender=lender)
        office = get_object_or_404(Office, pk=data['office'])
        if lender_partner.direct_partner:
            provider = lender_partner.direct_partner.user
        else:
            provider = get_object_or_404(User, username='donjuan')
        loan = Loan.objects.create(
            lender=lender,
            provider=provider,
            office=office,
            loan_type=data['loan_type'],
            value=data['value'],
            value_cop=data['value_cop'],
            interest=data['interest'],
            time=data['time'],
            exchange=data['exchange'],
            balance=data['value']
        )
        # if old_loan:
        #     data_1 = {
        #         'lender': lender,
        #         'request': data['request']
        #     }
        #     self.interest_load_payment(data_1)
        concept = get_object_or_404(Concept, name='Ingreso Préstamo Socio Directo')
        data = {
            'partner': lender_partner,
            'concept': concept,
            'movement_type': 'IN',
            'value': data['value'],
            'detail': 'Préstamo personal a socio {}'.format(lender_partner),
            'date': datetime.now(),
            'responsible': data['request'].user,
            'ip': get_ip(data['request'])
        }
        movement = MovementPartnerHandler.create_double(data)
        return loan

    def create_employee_loan(self, data):
        self.__validate_data(data)
        lender_employee = get_object_or_404(Employee, pk=data['lender'])
        lender = lender_employee.user
        old_loan = get_object_or_none(Loan, lender=lender)
        office = get_object_or_404(Office, pk=data['office'])

    def create_third_loan(self, data):
        self.__validate_data(data)
        lender = get_object_or_404(User, username='donjuan')
        donjuan = get_object_or_404(Partner, user=lender)
        office = get_object_or_404(Office, pk=data['office'])
        box_don_juan = BoxDonJuan.objects.get(partner=donjuan, office=office)
        concept = get_object_or_404(Concept, name='Ingreso Préstamo Terceros')
        provider, created = User.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            document_type=data['document_type'],
            document_id=data['document_id']
        )
        loan = Loan.objects.create(
            provider=provider,
            lender=lender,
            office=office,
            loan_type=data['loan_type'],
            value=data['value'],
            value_cop=data['value_cop'],
            interest=data['interest'],
            time=data['time'],
            exchange=data['exchange'],
            balance=data['value']
        )
        data = {
            'box': box_don_juan,
            'concept': concept,
            'movement_type': 'IN',
            'value': data['value'],
            'detail': 'Ingreso préstamo desde terceros',
            'date': datetime.now(),
            'responsible': data['request'].user,
            'ip': get_ip(data['request'])
        }
        print(data)
        movement = MovementDonJuanHandler.create(data)
        return loan

    def interest_load_payment(self, data):
        lender = data['lender']
        total_balance = Loan.objects.filter(lender=lender).aggregate(Sum('balance'))
        last_loan = Loan.objects.filter(lender=lender).last()
        interest = last_loan.interest
        total_interest = (total_balance * interest)/100
        concept = get_object_or_404(Concept, name='Pago Interés Préstamo Socio Directo')
        data = {
            'partner': lender.partner,
            'concept': concept,
            'movement_type': 'OUT',
            'value': total_interest,
            'detail': 'Pago interés prestamo socio directo',
            'date': datetime.now(),
            'responsible': data['request'].user,
            'ip': get_ip(data['request'])
        }
        movement = MovementPartnerHandler.create_double(data)


loan_manager = LoanManager()
