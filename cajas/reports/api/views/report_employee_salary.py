import requests

from datetime import date, timedelta

from django.db.models import Q
from django.http import JsonResponse

from rest_framework.views import APIView

from cajas.general_config.models.country import Country
from cajas.office.models import Office, OfficeCountry
from cajas.users.models import Employee


class ReportEmployeeSalary(APIView):

    def get(self, request):
        data = list()
        country_pk = request.query_params.get('country', None)
        office_country_pk = request.query_params.get('office_country', None)
        office_pk = request.query_params.get('office', None)
        employee_pk = request.query_params.get('employee', None)
        date_start = request.query_params.get('date_start', None)
        date_end = request.query_params.get('date_end', None)

        employees = Employee.objects.filter(user__related_collector_units__isnull=False).distinct()
        login = requests.get('http://external.vnmas.net/api/Session/Login/c184Ext/Gj7uQU')
        login = login.json()
        token = login[0]['data'][0]['user']['token']
        if employee_pk:
            employee = Employee.objects.get(pk=employee_pk)
            unit = employee.user.related_collector_units.get()
            unit_venda = requests.get(
                'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/{}/{}/{}'.format(
                    token,
                    date_start,
                    date_end,
                    unit.name,
                )
            )
            unit_venda = unit_venda.json()
            unit_values = unit_venda[0]['data'][0]['routeBalance']
            total_collection = int(unit_values['totCollection'])
            values = dict()
            values['employee'] = employee.__str__()
            values['total_collection'] = total_collection
            values['init_date'] = date_start
            values['end_date'] = date_end
            values['total_collection'] = total_collection
            if employee.salary_type == Employee.PERCENTAGE:
                values['value'] = (total_collection * employee.salary) / 100
            else:
                values['value'] = employee.salary
            data.append(values)
        if office_country_pk:
            office_country = OfficeCountry.objects.get(pk=office_country_pk)
            employees = employees.filter(
                Q(office_country=office_country) |
                Q(office=office_country.office)
            )
            for employee in employees:
                unit = employee.user.related_collector_units.get()
                unit_venda = requests.get(
                    'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/{}/{}/{}'.format(
                        token,
                        date_start,
                        date_end,
                        unit.name,
                    )
                )
                unit_venda = unit_venda.json()
                unit_values = unit_venda[0]['data'][0]['routeBalance']
                total_collection = int(unit_values['totCollection'])
                values = dict()
                values['employee'] = employee.__str__()
                values['total_collection'] = total_collection
                values['init_date'] = date_start
                values['end_date'] = date_end
                if employee.salary_type == Employee.PERCENTAGE:
                    values['value'] = (total_collection * employee.salary) / 100
                else:
                    values['value'] = employee.salary
                data.append(values)
        elif office_pk:
            office = Office.objects.get(pk=office_pk)
            for office_country in office.related_office_country.all():
                employees = employees.filter(
                    Q(office_country=office_country) |
                    Q(office=office_country.office)
                )
                for employee in employees:
                    unit = employee.user.related_collector_units.get()
                    unit_venda = requests.get(
                        'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/{}/{}/{}'.format(
                            token,
                            date_start,
                            date_end,
                            unit.name,
                        )
                    )
                    unit_venda = unit_venda.json()
                    unit_values = unit_venda[0]['data'][0]['routeBalance']
                    total_collection = int(unit_values['totCollection'])
                    values = dict()
                    values['employee'] = employee.__str__()
                    values['total_collection'] = total_collection
                    values['init_date'] = date_start
                    values['end_date'] = date_end
                    if employee.salary_type == Employee.PERCENTAGE:
                        values['value'] = (total_collection * employee.salary) / 100
                    else:
                        values['value'] = employee.salary
                    data.append(values)
        elif country_pk:
            country = Country.objects.get(pk=country_pk)
            office_countries = OfficeCountry.objects.filter(
                country=country
            )
            for office_country in office_countries:
                employees = employees.filter(
                    Q(office_country=office_country) |
                    Q(office=office_country.office)
                )
                for employee in employees:
                    unit = employee.user.related_collector_units.get()
                    unit_venda = requests.get(
                        'http://external.vnmas.net/api/Vmas/getInfoByPeriodAndRoute/{}/{}/{}/{}'.format(
                            token,
                            date_start,
                            date_end,
                            unit.name,
                        )
                    )
                    unit_venda = unit_venda.json()
                    unit_values = unit_venda[0]['data'][0]['routeBalance']
                    total_collection = int(unit_values['totCollection'])
                    values = dict()
                    values['employee'] = employee.__str__()
                    values['total_collection'] = total_collection
                    values['init_date'] = date_start
                    values['end_date'] = date_end
                    if employee.salary_type == Employee.PERCENTAGE:
                        values['value'] = (total_collection * employee.salary) / 100
                    else:
                        values['value'] = employee.salary
                    data.append(values)
        return JsonResponse(
            data,
            safe=False
        )
