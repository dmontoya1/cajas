
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from investments.models.investment import Investment
from office.models.office import Office


class InvestmentPaymentList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/investment_pay_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestmentPaymentList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        investment = get_object_or_404(Investment, pk=self.kwargs['pk'])
        context['investment'] = investment
        context['office'] = office
        return context
