
import requests

from django.db.models import Sum
from django.http import JsonResponse

from rest_framework.views import APIView

from cajas.loans.models.loan import Loan, LoanType
from cajas.users.models.partner import Partner


class ReportDebt(APIView):

    def get(self, request):
        data = dict()
        country = request.query_params.get('country', None)
        office_country = request.query_params.get('office_country', None)
        office = request.query_params.get('office', None)
        partner_pk = request.query_params.get('partner', None)
        if partner_pk:
            units_balance = 0
            base_route = 0
            partner = Partner.objects.get(pk=partner_pk)
            loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO).aggregate(Sum('value'))
            if loans['value__sum']:
                loan_value = loans['value__sum']
                units = partner.related_units.all()
                for u in units:

        if office_country:
            pass
        elif office:
            pass
        elif country:
            pass

        return JsonResponse(
            'TEST',
            safe=False
        )
