
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxPartner, BoxStatus
from cajas.office.models.officeCountry import OfficeCountry


class CloseoutBoxesList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/closeout_boxes_list.html'

    def get_context_data(self, **kwargs):
        context = super(CloseoutBoxesList, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        boxes = BoxPartner.objects.filter(Q(box_status=BoxStatus.EN_LIQUIDACION) | Q(box_status=BoxStatus.LIQUIDADA))
        context['boxes'] = boxes
        context['office'] = office
        return context
