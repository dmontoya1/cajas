
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from boxes.models.box_don_juan import BoxDonJuan
from concepts.models.concepts import Concept
from loans.models.loan import Loan, LoanType
from loans.models.loan_payments import LoanPayment
from movement.services.don_juan_service import DonJuanManager
from movement.services.partner_service import MovementPartnerManager
from movement.services.office_service import MovementOfficeManager
from webclient.views.get_ip import get_ip

from ..models.loan import Loan

movement_don_juan_manager = DonJuanManager()
movement_partner_manager = MovementPartnerManager()
movement_office_manager = MovementOfficeManager()
User = get_user_model()


class LoanPaymentManager(object):

    def add_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        self.create_payment(request)
        loan.balance -= int(request.data['value'])
        loan.save()

        if loan.loan_type == LoanType.EMPLEADO:
            if loan.provider:
                concept = get_object_or_404(Concept, name='Pago Abono préstamo empleado')
                data = {
                    'box': loan.office.box,
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
            data = {
                'partner': loan.lender.partner.get(),
                'box': loan.lender.partner.get().box,
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
            box_donjuan = get_object_or_404(BoxDonJuan, office=request.session['office'])
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

    def create_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        loan_payment = LoanPayment.objects.create(
            loan=loan,
            value=request.data['value'],
            date=request.data['date']
        )
        loan_payment.save()


loan_payment_manager = LoanPaymentManager()
