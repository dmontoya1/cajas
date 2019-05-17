
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from cajas.movement.models.movement_between_office_request import MovementBetweenOfficeRequest
from cajas.users.models.partner import Partner
from cajas.office.models.officeCountry import OfficeCountry


class MovementBetweenOfficesRequire(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/movement_between_offices.html'

    def get_context_data(self, **kwargs):
        context = super(MovementBetweenOfficesRequire, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser:
            movements = MovementBetweenOfficeRequest.objects.all()
        elif user.is_secretary:
            for office in user.related_employee.get().office.all():
                movements = MovementBetweenOfficeRequest.objects.filter(
                    box_office__office__office=office
                )
        context['movements'] = movements
        context['all_offices'] = OfficeCountry.objects.all().order_by('office')
        context['partners_offices'] = Partner.objects.all().exclude(code='DONJUAN')
        return context
