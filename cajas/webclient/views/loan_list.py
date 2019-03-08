
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.users.models.employee import Employee
from cajas.users.models.partner import Partner
from loans.models.loan import Loan
from office.models.office import Office

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
        office = get_object_or_404(Office, slug=slug)
        loans = Loan.objects.filter(office=office)
        partners = Partner.objects.filter(office=office)
        employees = Employee.objects.filter(office=office)
        context['office'] = office
        context['loans'] = loans
        context['partners'] = partners
        context['employees'] = employees
        return context
