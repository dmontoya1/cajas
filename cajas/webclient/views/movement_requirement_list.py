
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.movement.models.movement_request import MovementRequest


class MovementRequireList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/movement_require_list.html'

    def get_context_data(self, **kwargs):
        context = super(MovementRequireList, self).get_context_data(**kwargs)
        movements = MovementRequest.objects.all().exclude(concept__name='Retiro Socio Directo')
        context['movements'] = movements
        return context
