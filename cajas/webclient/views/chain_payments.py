
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.chains.models.chain import Chain
from cajas.office.models.officeCountry import OfficeCountry

User = get_user_model()


class ChainPayments(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/chain_payments.html'

    def get_context_data(self, **kwargs):
        context = super(ChainPayments, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        chain = get_object_or_404(Chain, pk=self.kwargs['pk'])
        context['office'] = office
        context['chain'] = chain
        return context
