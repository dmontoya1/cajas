
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.general_config.models.country import Country
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models import Employee


class ReportEmployeeSalary(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_employee_salary.html'

    def get_context_data(self, **kwargs):
        context = super(ReportEmployeeSalary, self).get_context_data(**kwargs)
        if self.request.user.is_secretary():
            employee = self.request.user.related_employee.get()
            offices = employee.office.all()
            offices_country = list()
            for o in offices:
                for oc in o.related_office_country.all():
                    offices_country.append(oc)
            context['offices_country'] = offices_country
            context['offices'] = offices
            context['employees'] = Employee.objects.filter(
                (Q(office__in=offices) | Q(office_country__in=offices_country)) &
                Q(user__related_collector_units__isnull=False)
            ).distinct()
        else:
            context['countries'] = Country.objects.all()
            context['offices'] = Office.objects.all()
            context['offices_country'] = OfficeCountry.objects.all()
            context['employees'] = Employee.objects.filter(user__related_collector_units__isnull=False).distinct()
        return context


