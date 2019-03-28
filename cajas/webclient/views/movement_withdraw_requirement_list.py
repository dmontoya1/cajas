
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from movement.models.movement_request import MovementRequest


class MovementWithdrawRequireList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/movement_withdraw_require_list.html'

    def get_context_data(self, **kwargs):
        context = super(MovementWithdrawRequireList, self).get_context_data(**kwargs)
        movements = MovementRequest.objects.filter(concept__name='Retiro Socio Directo')
        context['movements'] = movements
        return context
