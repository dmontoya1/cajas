
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest


class MovementBetweenOfficesRequire(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/movement_between_offices.html'

    def get_context_data(self, **kwargs):
        context = super(MovementBetweenOfficesRequire, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_secretary:
            for office in user.related_employee.get().office.all():
                movements = MovementBetweenOfficeRequest.objects.filter(
                    box_office__office__office=office
                )
        elif user.is_superuser:
            movements = MovementBetweenOfficeRequest.objects.all()
        context['movements'] = movements
        return context
