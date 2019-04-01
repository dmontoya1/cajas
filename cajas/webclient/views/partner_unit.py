
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from inventory.models import Category
from cajas.users.models.employee import Employee
from units.models.units import Unit
from office.models.office import Office
from cajas.users.models.partner import Partner


class PartnerUnitsList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/partner_unit.html'

    def get_context_data(self, **kwargs):
        context = super(PartnerUnitsList, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        slug = self.kwargs['slug']
        owner = get_object_or_404(Partner, pk=pk)
        office = get_object_or_404(Office, slug=slug)
        units = Unit.objects.filter(partner=owner)
        supervisor = Employee.objects.filter(office__pk=office.pk, charge__name="Supervisor", user__is_active=True)
        collectors = Employee.objects.filter(office__pk=office.pk, charge__name="Cobrador", user__is_active=True)
        categories = Category.objects.all()

        context['office'] = office
        context['units'] = units
        context['supervisor'] = supervisor
        context['collectors'] = collectors
        context['categories'] = categories
        context['owner'] = owner

        return context
