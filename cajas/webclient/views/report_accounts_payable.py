
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.chains.models.chain import Chain
from cajas.chains.models.chain_place import ChainPlace
from cajas.investments.models.investment import Investment
from cajas.loans.models.loan import Loan


class ReportAccountPayable(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_account_payable.html'

    def get_context_data(self, **kwargs):
        context = super(ReportAccountPayable, self).get_context_data(**kwargs)
        today = date.today()
        if self.request.user.is_superuser:
            context['loans'] = Loan.objects.filter(balance__gt=0)
            chains = []
            for c in Chain.objects.all():
                last_place = ChainPlace.objects.get(chain=c, name="Puesto {}".format(c.places))
                if last_place.pay_date >= today:
                    chains.append(c)
            context['chains'] = chains
            context['investments'] = Investment.objects.filter(balance__gt=0)
        elif self.request.user.related_employee.get().is_admin_charge():
            employee = self.request.user.related_employee.get()
            offices = employee.office.all()
            offices_country = list()
            for o in offices:
                for oc in o.related_office_country.all():
                    offices_country.append(oc)
            context['loans'] = Loan.objects.filter(office__in=offices_country, balance__gt=0)
            chains = []
            for c in Chain.objects.filter(office__in=offices_country):
                last_place = ChainPlace.objects.get(chain=c, name="Puesto {}".format(c.places))
                if last_place.pay_date >= today:
                    chains.append(c)
            context['chains'] = chains
            context['investments'] = Investment.objects.filter(partner__office__in=offices_country, balance__gt=0)

        return context
