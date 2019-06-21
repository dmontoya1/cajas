from datetime import timedelta, date, datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.office.models import Office
from cajas.users.models import AuthLogs, Employee, Charge


class ReportHours(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_hours.html'

    def get_context_data(self, **kwargs):
        context = super(ReportHours, self).get_context_data(**kwargs)
        office = Office.objects.get(number=self.kwargs['number'])
        start_date = self.request.GET.get('date_start', str(date.today()))
        end_date = self.request.GET.get('date_end', str(date.today()))
        charge = Charge.objects.get(name="Secretaria")
        secretaries = Employee.objects.filter(charge=charge, office=office)
        data = list()
        for secretary in secretaries:
            for single_date in self.date_range(start_date, end_date):
                hours = dict()
                hours['date'] = single_date
                hours['secretary'] = secretary
                if not single_date.weekday() == 6:
                    auth_login = AuthLogs.objects.filter(
                        user=secretary.user,
                        date__year=single_date.year,
                        date__month=single_date.month,
                        date__day=single_date.day,
                        action=AuthLogs.LOGIN,
                    ).first()
                    auth_logout = AuthLogs.objects.filter(
                        user=secretary.user,
                        date__year=single_date.year,
                        date__month=single_date.month,
                        date__day=single_date.day,
                        action=AuthLogs.LOGOUT,
                    ).last()
                    if auth_login:
                        hours['login'] = auth_login.date
                    else:
                        hours['login'] = auth_login
                    if auth_logout:
                        hours['logout'] = auth_logout.date
                    else:
                        hours['logout'] = auth_logout
                data.append(hours)
        context['data'] = data
        return context

    def date_range(self, start_date, end_date):
        end_date_1 = datetime.strptime(end_date, '%Y-%m-%d')
        end_date_1 = end_date_1 + timedelta(days=1)
        start_date_1 = datetime.strptime(start_date, '%Y-%m-%d')
        for n in range(int((end_date_1 - start_date_1).days)):
            yield start_date_1 + timedelta(n)
