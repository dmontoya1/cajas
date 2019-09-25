
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.concepts.models.concepts import Concept
from cajas.office.models.officeCountry import OfficeCountry


class BoxDonJuanOffice(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/donjuanbox.html'

    def get_context_data(self, **kwargs):
        context = super(BoxDonJuanOffice, self).get_context_data(**kwargs)
        concepts = Concept.objects.filter(is_active=True)
        office = get_object_or_404(OfficeCountry, slug=self.kwargs['slug'])
        box = get_object_or_404(BoxDonJuan, office=office)
        box_office = office.box
        if self.request.GET.get('all'):
            movements = box_office.movements.select_related('responsible', 'concept').all()
        else:
            movements = box_office.movements.select_related('responsible', 'concept').all()[:50]
        context['office'] = office
        context['box'] = box
        context['concepts'] = concepts
        context['offices'] = OfficeCountry.objects.select_related('office', 'country').all()
        context['movements'] = movements
        return context
