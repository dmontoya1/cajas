
from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from concepts.models.concepts import Concept
from loans.models.loan import Loan
from loans.models.loan_payments import LoanPayment
from movement.views.movement_partner.movement_partner_handler import MovementPartnerHandler
from webclient.views.get_ip import get_ip

from ..models.loan import Loan


User = get_user_model()


class LoanPaymentManager(object):

    def add_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        loan_payment = self.create_payment(request)
        concept = get_object_or_404(Concept, name='Pago Abono préstamo socio')
        data = {
            'partner': loan.lender.partner.get(),
            'concept': concept,
            'movement_type': 'OUT',
            'value': request.data['value'],
            'detail': 'Pago abono préstamo socio',
            'date': request.data['date'],
            'responsible': request.user,
            'ip': get_ip(request)
        }
        return MovementPartnerHandler.create_double(data)

    def create_payment(self, request):
        loan = get_object_or_404(Loan, pk=request.data['loan'])
        loan_payment = LoanPayment.objects.create(
            loan=loan,
            value=request.data['value'],
            date=request.data['date']
        )
        loan.save()
        return loan_payment


loan_payment_manager = LoanPaymentManager()
