
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.office_service import MovementOfficeManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.webclient.views.get_ip import get_ip

from ..models import Loan, LoanHistory

User = get_user_model()
donjuan_manager = DonJuanManager()
movement_parter_manager = MovementPartnerManager()
movement_office_manager = MovementOfficeManager()


class LoanManager(object):

    PROPERTIES = ['value', 'value_cop', 'interest', 'time', 'exchange', 'office', 'loan_type']

    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def create_partner_loan(self, data):
        self.__validate_data(data)
        lender_partner = get_object_or_404(Partner, pk=data['lender'])
        loan = Loan.objects.filter(lender=lender_partner.user).last()
        office = get_object_or_404(OfficeCountry, pk=data['office'])
        if lender_partner.direct_partner:
            provider = lender_partner.direct_partner
        else:
            provider = get_object_or_404(Partner, code='DONJUAN')
        if data['time'] == '':
            time = 0
        else:
            time = data['time']
        if not loan:
            loan = Loan.objects.create(
                lender=lender_partner.user,
                provider=provider,
                office=office,
                loan_type=data['loan_type'],
                value=data['value'],
                value_cop=data['value_cop'],
                interest=data['interest'],
                time=time,
                exchange=data['exchange'],
                balance=0
            )
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
        else:
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
            loan.interest = data['interest']
            loan.save()
        concept = get_object_or_404(Concept, name='Ingreso Préstamo Socio Directo')
        data = {
            'partner': lender_partner,
            'box': lender_partner.box,
            'concept': concept,
            'movement_type': 'IN',
            'value': data['value'],
            'detail': 'Préstamo sociedad a socio {}'.format(lender_partner),
            'date': datetime.now(),
            'responsible': data['request'].user,
            'ip': get_ip(data['request'])
        }
        movement_parter_manager.create_double(data)
        return loan

    def create_employee_loan(self, data):
        self.__validate_data(data)
        lender_employee = get_object_or_404(Employee, pk=data['lender'])
        lender = lender_employee.user
        old_loan = Loan.objects.filter(lender=lender).last()
        office = get_object_or_404(OfficeCountry, pk=data['office'])
        concept = get_object_or_404(Concept, name='Préstamo Personal Empleado')

        data_mov = {
            'concept': concept,
            'movement_type': 'OUT',
            'value': data['value'],
            'detail': 'Préstamo a empleado {}'.format(lender_employee),
            'date': datetime.now(),
            'responsible': data['request'].user,
            'ip': get_ip(data['request'])
        }
        if data['time'] == '':
            time = 0
        else:
            time = data['time']
        if not old_loan:
            if data['box_from'] == 'partner':
                provider = get_object_or_404(Partner, pk=data['provider'])
                loan = Loan.objects.create(
                    lender=lender,
                    provider=provider,
                    office=office,
                    loan_type=data['loan_type'],
                    value=data['value'],
                    value_cop=data['value_cop'],
                    interest=data['interest'],
                    time=time,
                    exchange=data['exchange'],
                    balance=0
                )
                data_mov['box'] = provider.box
                data_mov['partner'] = provider
                movement = movement_parter_manager.create_simple(data_mov)
            elif data['box_from'] == 'donjuan':
                provider = get_object_or_404(Partner, code='DONJUAN')
                loan = Loan.objects.create(
                    lender=lender,
                    provider=provider,
                    office=office,
                    loan_type=data['loan_type'],
                    value=data['value'],
                    value_cop=data['value_cop'],
                    interest=data['interest'],
                    time=time,
                    exchange=data['exchange'],
                    balance=0
                )
                data_mov['box'] = BoxDonJuan.objects.get(office=office)
                movement = donjuan_manager.create_movement(data_mov)
            else:
                loan = Loan.objects.create(
                    lender=lender,
                    office=office,
                    loan_type=data['loan_type'],
                    value=data['value'],
                    value_cop=data['value_cop'],
                    interest=data['interest'],
                    time=time,
                    exchange=data['exchange'],
                    balance=0
                )
                data_mov['box_office'] = office.box
                movement = movement_office_manager.create_movement(data_mov)
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
        else:
            LoanHistory.objects.create(
                loan=old_loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
            old_loan.interest = data['interest']
            old_loan.save()

    def create_third_loan(self, data):
        self.__validate_data(data)
        lender = get_object_or_404(User, username='donjuan')
        donjuan = get_object_or_404(Partner, user=lender)
        office = get_object_or_404(OfficeCountry, pk=data['office'])
        box_don_juan = BoxDonJuan.objects.get(partner=donjuan, office=office)
        concept = get_object_or_404(Concept, name='Ingreso Préstamo Terceros')
        provider, created = User.objects.get_or_create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            document_type=data['document_type'],
            document_id=data['document_id']
        )
        old_loan = Loan.objects.filter(lender=lender, provider=provider).last()
        if not old_loan:
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
                balance=0
            )
            LoanHistory.objects.create(
                loan=loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
        else:
            LoanHistory.objects.create(
                loan=old_loan,
                history_type=LoanHistory.LOAN,
                movement_type=LoanHistory.IN,
                value=data['value'],
                value_cop=data['value_cop'],
                date=datetime.now()
            )
            old_loan.interest = data['interest']
            old_loan.save()
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
        movement = donjuan_manager.create_movement(data)
        return loan



