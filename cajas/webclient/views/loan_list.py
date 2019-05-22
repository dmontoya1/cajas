
from datetime import datetime

from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from cajas.general_config.models.exchange import Exchange
from cajas.loans.models.loan import Loan
from cajas.office.models.officeCountry import OfficeCountry
from cajas.webclient.views.utils import get_object_or_none

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

        try:
            if self.request.user.is_superuser or self.request.user.related_employee.get().is_admin_charge():
                context['loans'] = Loan.objects.filter(office=office)
                context['partners'] = Partner.objects.filter(office=office, is_active=True)
                context['employees'] = Employee.objects.filter(
                    Q(user__is_active=True) &
                    (Q(office_country=office) | Q(office=office.office))
                )
                now = datetime.now()
                context['exchange'] = get_object_or_none(
                    Exchange,
                    currency=office.country.currency,
                    month__month=now.month,
                )
        except Exception as e:
            context['loans'] = Loan.objects.filter(office=office, lender=self.request.user)
        context['office'] = office
        return context
