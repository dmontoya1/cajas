
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from office.models.office import Office


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
                if user.related_employee.get().is_admin_charge:
                    print(user.related_employee.get().office.all())
                    context['offices'] = user.related_employee.get().office.all()
                else:
                    context['offices'] = user.related_employee.get().office_country.all()
            except Exception as e:
                print(e)
                pass
        else:
            context['offices'] = Office.objects.all()
        return context
