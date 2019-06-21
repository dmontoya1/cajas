from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models import Employee, DailySquareUnits
from cajas.users.models.group_employee import GroupEmployee
from cajas.users.models.group import Group
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.webclient.views.utils import get_object_or_none


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
        units = Unit.objects.filter(Q(partner__office=office) |
                                    (Q(partner__code='DONJUAN') &
                                     (Q(collector__related_employee__office_country=office) |
                                      Q(collector__related_employee__office=office.office) |
                                      Q(supervisor__related_employee__office_country=office) |
                                      Q(supervisor__related_employee__office=office.office)
                                      ))).distinct()
        try:
            employee = Employee.objects.get(
                Q(user=self.request.user) & (Q(office=office.office) | Q(office_country=office)))
            group = get_object_or_none(DailySquareUnits, employee=employee)
            if group and group.units.all().exists():
                units = group.units.filter(partner__office=office)
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

        if str(employee.charge) == "Administrador de Grupo":
            try:
                group = get_object_or_404(Group, admin=employee)
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
        context['units'] = units
        context['supervisors'] = superv
        return context
