
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from units.models.units import Unit
from office.models.office import Office


class UnitsList(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/units_list.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeItemsList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        units = Unit.objects.filter(partner__office=office)
        print(units)
        return context
