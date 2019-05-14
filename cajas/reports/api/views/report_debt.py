
import requests
from datetime import date

from django.db.models import Sum
from django.http import JsonResponse

from rest_framework.views import APIView

from cajas.general_config.models.country import Country
from cajas.loans.models.loan import Loan, LoanType
from cajas.office.models import Office, OfficeCountry
from cajas.users.models.partner import Partner


class ReportDebt(APIView):

    def get(self, request):
        data = list()
        country_pk = request.query_params.get('country', None)
        office_country_pk = request.query_params.get('office_country', None)
        office_pk = request.query_params.get('office', None)
        partner_pk = request.query_params.get('partner', None)
        login = requests.get('http://external.vnmas.net/api/Session/Login/c184Ext/Gj7uQU')
        login = login.json()
        token = login[0]['data'][0]['user']['token']
        now = date.today()
        today = now.strftime('%Y%m%d')
        if partner_pk:
            debt_level = 0
            final_total_balance = 0
            cash_balance = 0
            partner = Partner.objects.get(pk=partner_pk)
            loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO).aggregate(Sum('balance'))
            if loans['balance__sum']:

                loan_value = loans['balance__sum']
                units = partner.related_units.all()
                for u in units:
                    unit_venda = requests.get(
                        'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/20180101/{}/{}'.format(
                            token,
                            today,
                            u.name,
                        )
                    )
                    unit_venda = unit_venda.json()
                    unit_values = unit_venda[0]['data'][0]['routeBalance']
                    final_total_balance += int(unit_values['finalTotalBalance'])
                    cash_balance += int(unit_values['cashBalance'])
                    debt_level = (partner.box.balance + final_total_balance + cash_balance) / loan_value
            values = dict()
            values['partner'] = partner.__str__()
            values['level'] = debt_level
            data.append(values)
        elif office_country_pk:
            office_country = OfficeCountry.objects.get(pk=office_country_pk)
            partners = Partner.objects.filter(
                office=office_country
            )
            for partner in partners:
                debt_level = 0
                final_total_balance = 0
                cash_balance = 0
                loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO).aggregate(
                    Sum('balance'))
                if loans['balance__sum']:
                    loan_value = loans['balance__sum']
                    units = partner.related_units.all()
                    for u in units:
                        unit_venda = requests.get(
                            'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/20190101/{}/{}'.format(
                                token,
                                today,
                                u.name,
                            )
                        )
                        unit_venda = unit_venda.json()
                        unit_values = unit_venda[0]['data'][0]['routeBalance']
                        final_total_balance += int(unit_values['finalTotalBalance'])
                        cash_balance += int(unit_values['cashBalance'])
                        debt_level = (partner.box.balance + final_total_balance + cash_balance) / loan_value
                values = dict()
                values['partner'] = partner.__str__()
                values['level'] = debt_level
                data.append(values)
        elif office_pk:
            office = Office.objects.get(pk=office_pk)
            for office_country in office.related_office_country.all():
                partners = Partner.objects.filter(
                    office=office_country
                )
                for partner in partners:
                    debt_level = 0
                    final_total_balance = 0
                    cash_balance = 0
                    loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO).aggregate(
                        Sum('balance'))
                    if loans['balance__sum']:
                        loan_value = loans['balance__sum']
                        units = partner.related_units.all()
                        for u in units:
                            unit_venda = requests.get(
                                'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/20190101/{}/{}'.format(
                                    token,
                                    today,
                                    u.name,
                                )
                            )
                            unit_venda = unit_venda.json()
                            unit_values = unit_venda[0]['data'][0]['routeBalance']
                            final_total_balance += int(unit_values['finalTotalBalance'])
                            cash_balance += int(unit_values['cashBalance'])
                            debt_level = (partner.box.balance + final_total_balance + cash_balance) / loan_value
                    values = dict()
                    values['partner'] = partner.__str__()
                    values['level'] = debt_level
                    data.append(values)
        elif country_pk:
            country = Country.objects.get(pk=country_pk)
            office_countries = OfficeCountry.objects.filter(
                country=country
            )
            for office_country in office_countries:
                partners = Partner.objects.filter(
                    office=office_country
                )
                for partner in partners:
                    debt_level = 0
                    final_total_balance = 0
                    cash_balance = 0
                    loans = Loan.objects.filter(lender=partner.user, loan_type=LoanType.SOCIO_DIRECTO).aggregate(
                        Sum('balance'))
                    if loans['balance__sum']:
                        loan_value = loans['balance__sum']
                        units = partner.related_units.all()
                        for u in units:
                            unit_venda = requests.get(
                                'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/20190101/{}/{}'.format(
                                    token,
                                    today,
                                    u.name,
                                )
                            )
                            unit_venda = unit_venda.json()
                            unit_values = unit_venda[0]['data'][0]['routeBalance']
                            final_total_balance += int(unit_values['finalTotalBalance'])
                            cash_balance += int(unit_values['cashBalance'])
                            debt_level = (partner.box.balance + final_total_balance + cash_balance) / loan_value
                    values = dict()
                    values['partner'] = partner.__str__()
                    values['level'] = debt_level
                    data.append(values)
        return JsonResponse(
            data,
            safe=False
        )
