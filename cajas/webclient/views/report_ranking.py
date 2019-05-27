
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class ReportRanking(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_ranking.html'
