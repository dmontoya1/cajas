
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.general_config.models.country import Country
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.partner import Partner


class ReportDebt(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_debt.html'

    def get_context_data(self, **kwargs):
        context = super(ReportDebt, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['offices'] = Office.objects.all()
        context['offices_country'] = OfficeCountry.objects.all()
        context['partners'] = Partner.objects.all()
        return context


