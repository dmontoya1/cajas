

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
        try:
            del request.session['office']
        except KeyError:
            pass

        return super(Home, self).get(request)

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        countries = Country.objects.all()
        context['countries'] = countries
        return context
