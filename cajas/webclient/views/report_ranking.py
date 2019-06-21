
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.office.models import Office


class ReportRanking(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_ranking.html'

    def get_context_data(self, **kwargs):
        context = super(ReportRanking, self).get_context_data(**kwargs)
        office = Office.objects.filter(~Q(number=0))
        context['offices'] = office
        context['range'] = range(office.count())
        return context
