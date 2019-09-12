import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.charges import Charge
from cajas.users.models.employee import Employee
from cajas.office.models.officeCountry import OfficeCountry
from .utils import is_secretary, is_admin_senior

logger = logging.getLogger(__name__)


class EmployeeList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/employee_list.html'

    def get(self, request, slug):
        office = OfficeCountry.objects.get(slug=slug)
        request.session['office'] = office.pk
        return super(EmployeeList, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        try:
            if (self.request.user.is_superuser or is_secretary(self.request.user, office) or
                 is_admin_senior(self.request.user, office)):
                context['employees'] = Employee.objects.filter(office_country=office, user__is_active=True)
                context['employees1'] = Employee.objects.filter(office=office.office, user__is_active=True)
                context['charges'] = Charge.objects.all().exclude(name="Presidente")
            else:
                context['employees'] = Employee.objects.filter(office_country=office, user=self.request.user)
        except Exception as e:
            logger.exception(str(e))
            context['employees'] = Employee.objects.filter(office_country=office, user=self.request.user)

        context['office'] = office
        context['groups'] = Group.objects.all()
        return context
