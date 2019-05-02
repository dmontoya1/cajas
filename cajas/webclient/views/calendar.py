
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.group_employee import GroupEmployee
from cajas.users.models.group import Group
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit


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
        superv = {}
        context['office'] = office
        context['units'] = Unit.objects.filter(partner__office=office)

        try:
            user = self.request.user.related_employee.get()
        except:
            if self.request.user.is_superuser:
                superv = Employee.objects.filter(
                    (Q(office_country=office) |
                     Q(office=office.office)) &
                    Q(user__is_active=True)
                )
            else:
                superv = []
            context['supervisors'] = superv
            return context

        if str(user.charge) == "Administrador de Grupo":
            try:
                group = get_object_or_404(Group, admin=user)
                superv = GroupEmployee.objects.filter(
                    group=group,
                )
            except Exception as e:
                print(e)
        else:
            superv = Employee.objects.filter(
                (Q(office_country=office) |
                 Q(office=office.office)) &
                Q(user__is_active=True)
            )

        context['supervisors'] = superv
        return context
