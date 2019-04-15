
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee
from office.models.officeCountry import OfficeCountry


class EmployeeList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/employee_list.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        employees = Employee.objects.filter(office_country=office, user__is_active=True)
        employees1 = Employee.objects.filter(office=office.office, user__is_active=True)
        charges = Charge.objects.all().exclude(name="Presidente")

        context['office'] = office
        context['employees'] = employees
        context['employees1'] = employees1
        context['charges'] = charges
        return context
