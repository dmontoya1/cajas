
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from inventory.models import Category
from cajas.users.models.employee import Employee
from units.models.units import Unit
from office.models.office import Office
from cajas.users.models.partner import Partner


class UnitsList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/units_list.html'

    def get_context_data(self, **kwargs):
        context = super(UnitsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        units = Unit.objects.filter(partner__office=office)
        supervisor = Employee.objects.filter(office__pk=office.pk, charge__name="Supervisor", user__is_active=True)
        collectors = Employee.objects.filter(office__pk=office.pk, charge__name="Cobrador", user__is_active=True)
        partners = Partner.objects.filter(office__pk=office.pk, user__is_active=True).exclude(partner_type='DJ')
        categories = Category.objects.all()

        context['office'] = office
        context['units'] = units
        context['supervisor'] = supervisor
        context['collectors'] = collectors
        context['partners'] = partners
        context['categories'] = categories

        print(partners)
        return context
