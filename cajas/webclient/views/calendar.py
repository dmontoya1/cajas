
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from office.models.officeCountry import OfficeCountry
from cajas.users.models.group_employee import GroupEmployee


class Calendar(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/calendar.html'

    def get_context_data(self, **kwargs):
        context = super(Calendar, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        if self.request.user.related_employee.get().charge == "Administrador de Grupo":
            try:
                supervisor = GroupEmployee.objects.get(
                    group__user=self.request.user,
                ).supervisor
            except Exception as e:
                print(e)
        else:
            supervisor = Employee.objects.filter(office_country=office, charge__name="Supervisor", user__is_active=True)
        context['office'] = office
        context['supervisors'] = supervisor

        return context
