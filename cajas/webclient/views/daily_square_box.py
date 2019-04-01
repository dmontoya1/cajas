
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from office.models.office import Office
from units.models.units import Unit


class DailySquareBox(LoginRequiredMixin, TemplateView):
    """Ver la caja de un usuario Cuadre diario
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_box.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareBox, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(Office, slug=slug)
        user_pk = self.kwargs['pk']
        user = User.objects.get(pk=user_pk)
        users = User.objects.filter(Q(partner__office=office) or Q(employee__office=office))
        box_daily_square = get_object_or_404(BoxDailySquare, user=user)
        offices = Office.objects.all()
        partners = Partner.objects.filter(office=box_daily_square.office).order_by('user__first_name')
        units = Unit.objects.filter(partner__office=office)
        context['box'] = box_daily_square
        context['offices'] = offices
        context['office'] = office
        context['partners'] = partners
        context['box_user'] = user
        context['users'] = users
        context['units'] = units
        return context
