
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.users.models.partner import Partner
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry


class Reports(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/reports.html'

    def get_context_data(self, **kwargs):
        context = super(Reports, self).get_context_data(**kwargs)
        context['all_offices'] = OfficeCountry.objects.all().order_by('office')
        context['partners_offices'] = Partner.objects.all().exclude(code='DONJUAN')
        return context
