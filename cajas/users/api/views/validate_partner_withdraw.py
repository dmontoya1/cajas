
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.users.models.partner import Partner
from cajas.loans.models.loan import Loan, LoanType


class ValidatePartnerWithdraw(APIView):

    def post(self, request):
        data = request.data
        validate = self.validate_withdraw(data)
        if validate == 'loan':
            return Response(
                "El socio tiene préstamos activos.",
                status=status.HTTP_202_ACCEPTED
            )
        elif validate == 'value':
            return Response(
                "El socio no tiene los fondos suficientes en su caja para realizar el retiro.",
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                "Validación exitosa. El socio puede hacer el retiro.",
                status=status.HTTP_200_OK
            )

    def validate_withdraw(self, data):
        if self.validate_loans(data):
            return 'loan'
        elif not self.validate_value(data):
            return 'value'
        return True

    def validate_loans(self, data):
        partner = get_object_or_404(Partner, pk=data['partner'])
        loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO)
        if loans.exists():
            for loan in loans:
                if loan.balance > 0:
                    return True
            return False
        return False

    def validate_value(self, data):
        partner = get_object_or_404(Partner, pk=data['partner'])
        box = partner.box
        if (int(data['value']) * 3) < box.balance:
            return True
        return False
