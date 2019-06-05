
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
        if self.request.user.is_secretary():
            employee = self.request.user.related_employee.get()
            offices = employee.office.all()
            offices_country = list()
            for o in offices:
                for oc in o.related_office_country.all():
                    offices_country.append(oc)
            parners = Partner.objects.filter(office__in=offices_country)
            context['offices_country'] = offices_country
            context['offices'] = offices
            context['partners'] = parners
        else:
            context['countries'] = Country.objects.all()
            context['offices'] = Office.objects.all()
            context['offices_country'] = OfficeCountry.objects.all()
            context['partners'] = Partner.objects.all()
        return context


