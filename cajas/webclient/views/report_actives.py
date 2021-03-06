
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.inventory.models.brand import Brand
from cajas.general_config.models.country import Country
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry


class ReportActives(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/report_actives.html'

    def get_context_data(self, **kwargs):
        context = super(ReportActives, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['countries'] = Country.objects.all()
            context['offices'] = Office.objects.all()
            context['offices_country'] = OfficeCountry.objects.all()
        else:
            employee = self.request.user.related_employee.get()
            offices = employee.office.all()
            offices_country = list()
            for o in offices:
                for oc in o.related_office_country.all():
                    offices_country.append(oc)
            context['offices_country'] = offices_country
            context['offices'] = offices
        context['brands'] = Brand.objects.all()
        return context
