
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from general_config.models.exchange import Exchange
from loans.models.loan import Loan
from office.models.office import Office
from webclient.views.utils import get_object_or_none

User = get_user_model()


class LoanPaymentList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/loan_payment_list.html'

    def get_context_data(self, **kwargs):
        context = super(LoanPaymentList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        loan = get_object_or_404(Loan, pk=self.kwargs['pk'])
        context['loan'] = loan
        context['office'] = office
        return context
