
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from inventory.models import Category
from office.models.officeCountry import OfficeCountry
from units.models.units import Unit


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
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['units'] = Unit.objects.filter(partner__office=office)
                context['employees'] = Employee.objects.filter(
                    Q(office_country=office) |
                    Q(office=office.office) &
                    Q(user__is_active=True)
                )
                context['partners'] = Partner.objects.filter(office=office, user__is_active=True).exclude(partner_type='DJ')
                context['categories'] = Category.objects.all()
        except Exception as e:
            partner = Partner.objects.get(user=self.request.user, office=office)
            context['units'] = Unit.objects.filter(partner__office=office, partner=partner)

        employees = Employee.objects.filter(office_country=office, user__is_active=True)
        context['employees'] = employees
        context['office'] = office

        return context
