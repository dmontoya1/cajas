
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.partner import Partner
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
        try:
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                investments = Investment.objects.filter(partner__office=office)
        except Exception as e:
            partner = Partner.objects.get(user=self.request.user, office=office)
            investments = Investment.objects.filter(partner=partner)
        context['office'] = office
        context['investments'] = investments
        return context
