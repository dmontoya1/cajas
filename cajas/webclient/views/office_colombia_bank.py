
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from boxes.models.box_colombia import BoxColombia
from office.models.officeCountry import OfficeCountry


class OfficeColombiaBank(LoginRequiredMixin, TemplateView):
    """Ver la caja de una oficina
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/office_colombia_bank.html'

    def get_context_data(self, **kwargs):
        context = super(OfficeColombiaBank, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['box'] = get_object_or_404(BoxColombia, name='Caja Banco')
        context['office'] = office
        return context
