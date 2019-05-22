
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.users.models.partner import Partner
from cajas.office.models.office import Office
from cajas.office.models.officeCountry import OfficeCountry


class Home(LoginRequiredMixin, TemplateView):
    """
    """
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/home.html'

    def get(self, request, format=None):
        if 'office' in request.session:
            del request.session['office']
        return super(Home, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        user = self.request.user

        if not self.request.user.is_superuser:
            try:
                if user.related_employee.get().is_admin_charge():
                    if user.related_employee.get().office.all().exists():
                        context['offices'] = user.related_employee.get().office.all()
                    else:
                        context['offices_country'] = user.related_employee.get().office_country.all()
                else:
                    context['offices'] = user.related_employee.get().office_country.all()
            except Exception as e:
                print(e)
                context['actual_partners'] = Partner.objects.filter(user=user)
        else:
            context['offices'] = Office.objects.all()
            context['all_offices'] = OfficeCountry.objects.all().order_by('office')
            context['partners_offices'] = Partner.objects.all().exclude(code='DONJUAN')
        print("Contexto -->", context)
        return context
