
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from office.models.office import Office

from concepts.models.concepts import Concept
from movement.models.movement_provisioning import MovementProvisioning


class Provisioning(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/provisioning.html'

    def get_context_data(self, **kwargs):
        slug = self.kwargs['slug']
        context = super(Provisioning, self).get_context_data(**kwargs)
        concept = get_object_or_404(Concept, name="Aprovisionamiento Oficina")
        provisioning = MovementProvisioning.objects.filter(box_provisioning__office__slug=slug)
        office = get_object_or_404(Office, slug=slug)
        context['office'] = office
        context['concept'] = concept
        context['provisioning'] = provisioning

        return context
