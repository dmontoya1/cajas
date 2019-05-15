
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.inventory.models.brand import Brand
from cajas.general_config.models.country import Country
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry


class ReportEmployeeSalary(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_employee_salary.html'

    def get_context_data(self, **kwargs):
        context = super(ReportEmployeeSalary, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['offices'] = Office.objects.all()
        context['offices_country'] = OfficeCountry.objects.all()
        context['brands'] = Brand.objects.all()
        return context


