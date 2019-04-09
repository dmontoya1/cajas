
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from general_config.models.exchange import Exchange
from loans.models.loan import Loan
from office.models.officeCountry import OfficeCountry
from webclient.views.utils import get_object_or_none

User = get_user_model()


class LoanList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/loan_list.html'

    def get_context_data(self, **kwargs):
        context = super(LoanList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        loans = Loan.objects.filter(office=office)
        partners = Partner.objects.filter(office=office)
        employees = Employee.objects.filter(office_country=office, office=office.office)
        now = datetime.now()
        exchange = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=now.month,
        )
        context['office'] = office
        context['loans'] = loans
        context['partners'] = partners
        context['employees'] = employees
        context['exchange'] = exchange
        return context
