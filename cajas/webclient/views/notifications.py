
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.office.models.officeCountry import OfficeCountry
from cajas.office.models.notifications import Notifications as Notify


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
        notifications = Notify.objects.filter(office=office)
        context['office'] = office
        context['notifications'] = notifications

        return context
