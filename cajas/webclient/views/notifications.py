
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from office.models.officeCountry import OfficeCountry


class Notifications(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/notifications.html'

    def get_context_data(self, **kwargs):
        context = super(Notifications, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        context['office'] = office
        return context
