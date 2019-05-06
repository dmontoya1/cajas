
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.movement.models.movement_withdraw import MovementWithdraw


class MovementWithdrawRequireList(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/movement_withdraw_require_list.html'

    def get_context_data(self, **kwargs):
        context = super(MovementWithdrawRequireList, self).get_context_data(**kwargs)
        movements = MovementWithdraw.objects.all()
        context['movements'] = movements
        return context
