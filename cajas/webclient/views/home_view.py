

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from general_config.models.country import Country


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
        if not self.request.user.is_superuser:
            try:
                context['office'] = self.request.user.employee.office
            except:
                context['office'] = self.request.user.partner.get().office
        else:
            context['countries'] = Country.objects.all()
        return context
