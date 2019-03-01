
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from boxes.models.box_don_juan import BoxDonJuan
from concepts.models.concepts import Concept
from office.models.office import Office


class BoxDonJuanOffice(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/donjuanbox.html'

    def get_context_data(self, **kwargs):
        context = super(BoxDonJuanOffice, self).get_context_data(**kwargs)
        concepts = Concept.objects.filter(is_active=True)
        office = get_object_or_404(Office, slug=self.kwargs['slug'])
        box = get_object_or_404(BoxDonJuan, office=office)
        context['office'] = office
        context['box'] = box
        context['concepts'] = concepts
        return context
