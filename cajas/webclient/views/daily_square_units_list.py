from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models import Unit
from cajas.users.models import User, DailySquareUnits, Employee
from cajas.webclient.views.utils import get_president_user

president = get_president_user()


class DailySquareUnitsList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_units_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareUnitsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        user_pk = self.kwargs['pk']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        employee = Employee.objects.get(pk=user_pk)
        daily_square_group, created = DailySquareUnits.objects.get_or_create(
            employee=employee
        )
        context['employee'] = employee
        context['units'] = daily_square_group.units.all()
        context['units_office'] = Unit.objects.filter(Q(partner__office=office) |
                                                      (Q(partner__user=president) &
                                                       (Q(collector__related_employee__office_country=office) |
                                                        Q(collector__related_employee__office=office.office)
                                                        ))).distinct()
        return context
