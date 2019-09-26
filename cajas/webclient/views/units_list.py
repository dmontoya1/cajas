
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.inventory.models import Category
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.webclient.views.utils import get_president_user

from .utils import is_admin_senior, is_secretary

logger = logging.getLogger(__name__)
president = get_president_user()


class UnitsList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/units_list.html'

    def get_context_data(self, **kwargs):
        context = super(UnitsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        try:
            if self.request.user.is_superuser or is_secretary(self.request.user, office) or \
                is_admin_senior(self.request.user, office):
                context['units'] = Unit.objects.select_related(
                    'partner', 'partner__user', 'collector', 'supervisor'
                ).filter(Q(partner__office=office) |
                           (Q(partner__user=president) &
                            (Q(collector__related_employee__office_country=office) |
                             Q(collector__related_employee__office=office.office)
                             ))).distinct()
                context['employees'] = Employee.objects.select_related(
                    'user', 'charge',
                ).filter(
                    Q(office_country=office) |
                    Q(office=office.office) &
                    Q(user__is_active=True)
                )
                context['partners'] = Partner.objects.select_related(
                        'office', 'box', 'user', 'office__country', 'office__country__currency'
                ).filter(
                    (Q(office=office) & Q(user__is_active=True)) |
                    Q(user=president)
                )
                context['categories'] = Category.objects.all()
            else:
                partner = Partner.objects.get(user=self.request.user, office=office)
                context['units'] = Unit.objects.filter(partner__office=office, partner=partner)
        except Exception as e:
            logger.exception(str(e))
            partner = Partner.objects.get(user=self.request.user, office=office)
            context['units'] = Unit.objects.filter(partner__office=office, partner=partner)

        context['office'] = office

        return context
