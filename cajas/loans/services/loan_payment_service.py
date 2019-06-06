
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.boxes.models import BoxDonJuan, BoxPartner
from cajas.concepts.models.concepts import Concept
from cajas.loans.models.loan import Loan, LoanType
from cajas.loans.models.loan_history import LoanHistory
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.movement.services.office_service import MovementOfficeManager
from cajas.office.models import OfficeCountry
from cajas.users.models import Partner
from cajas.webclient.views.get_ip import get_ip

from ..models.loan import Loan

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
                concept = get_object_or_404(Concept, name='Pago Abono préstamo socio')
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
        LoanHistory.objects.create(
            loan=loan,
            history_type=LoanHistory.ABONO,
            movement_type=LoanHistory.OUT,
            value=request.data['value'],
            value_cop=request.data['value_cop'],
            date=request.data['date']
        )

    def interest_load_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        LoanHistory.objects.create(
            loan=loan,
            history_type=LoanHistory.INTEREST,
            movement_type=LoanHistory.OUT,
            value=request.data['value'],
            value_cop=request.data['value_cop'],
            date=datetime.now()
        )
