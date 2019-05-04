
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from chains.models.chain import Chain
from chains.models.chain_place import ChainPlace
from investments.models.investment import Investment
from loans.models.loan import Loan


class ReportAccountPayable(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_account_payable.html'

    def get_context_data(self, **kwargs):
        context = super(ReportAccountPayable, self).get_context_data(**kwargs)
        today = date.today()
        context['loans'] = Loan.objects.filter(balance__gt=0)
        chains = []
        for c in Chain.objects.all():
            last_place = ChainPlace.objects.get(chain=c, name="Puesto {}".format(c.places))
            if last_place.pay_date >= today:
                chains.append(c)
        context['chains'] = chains
        context['investments'] = Investment.objects.filter(balance__gt=0)
        return context
