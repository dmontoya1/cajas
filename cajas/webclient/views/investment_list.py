
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from investments.models.investment import Investment
from office.models.officeCountry import OfficeCountry


class InvestmentList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/investment_list.html'

    def get_context_data(self, **kwargs):
        context = super(InvestmentList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        investments = Investment.objects.filter(partner__office=office)
        context['office'] = office
        context['investments'] = investments
        return context
