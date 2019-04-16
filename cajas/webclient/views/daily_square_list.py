from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from units.models.units import Unit
from office.models.officeCountry import OfficeCountry


class DailySquareList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_list.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        offices = OfficeCountry.objects.all()
        units = Unit.objects.filter(partner__office=office)
        users = User.objects.filter(Q(partner__office=office) | Q(related_employee__office_country=office) |
                                    Q(related_employee__office=office.office))
        try:
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['dailys'] = User.objects.filter(
                    Q(is_daily_square=True) &
                    (Q(related_employee__office=office.office) |
                     Q(partner__office=office) |
                     Q(related_employee__office_country=office)
                     )
                ).distinct()
        except Exception as e:
            print(e)
            context['partner'] = self.request.user.partner.get()
        context['offices'] = offices
        context['units'] = units
        context['users'] = users

        return context
