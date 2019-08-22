from datetime import datetime, date, timedelta

from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.general_config.models.exchange import Exchange
from cajas.users.models.partner import Partner
from cajas.users.models.user import User
from cajas.inventory.models import Category
from cajas.movement.models.movement_daily_square import MovementDailySquare
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.users.models import Employee, DailySquareUnits
from cajas.webclient.views.utils import get_object_or_none


class DailySquareBox(LoginRequiredMixin, TemplateView):
    """Ver la caja de un usuario Cuadre diario
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/daily_square_box.html'

    def get_context_data(self, **kwargs):
        context = super(DailySquareBox, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        office = get_object_or_404(OfficeCountry, slug=slug)
        user_pk = self.kwargs['pk']
        user = User.objects.get(pk=user_pk)
        users = User.objects.filter(Q(partner__office=office) | Q(related_employee__office_country=office) |
                                    Q(related_employee__office=office.office))
        box_daily_square = get_object_or_404(BoxDailySquare, user=user, office=office)
        offices = OfficeCountry.objects.all()
        partners = Partner.objects.filter(
            Q(office=box_daily_square.office) | Q(code='DONJUAN')).order_by('user__first_name')
        dq_list = User.objects.filter(
            (Q(partner__office=office) | Q(related_employee__office_country=office) |
             Q(related_employee__office=office.office)) &
            Q(is_daily_square=True)).distinct()
        context['dq_list'] = dq_list
        if self.request.GET.get('all'):
            movements = box_daily_square.movements.all()
        else:
            movements = box_daily_square.movements.all()[:50]
        try:
            employee = Employee.objects.get(
                Q(user=user) & Q(office_country=office))
            group = get_object_or_none(DailySquareUnits, employee=employee)
            if group and group.units.all().exists():
                units = group.units.filter(Q(partner__office=office) |
                                            (Q(partner__code='DONJUAN') &
                                             (Q(collector__related_employee__office_country=office) |
                                              Q(collector__related_employee__office=office.office)
                                              ))).distinct()
            else:
                units = Unit.objects.filter(Q(partner__office=office) |
                                            (Q(partner__code='DONJUAN') &
                                             (Q(collector__related_employee__office_country=office) |
                                              Q(collector__related_employee__office=office.office)
                                              ))).distinct()
        except Employee.DoesNotExist:
            units = Unit.objects.filter(Q(partner__office=office) |
                                        (Q(partner__code='DONJUAN') &
                                         (Q(collector__related_employee__office_country=office) |
                                          Q(collector__related_employee__office=office.office)
                                          ))).distinct()
        past_mvments = MovementDailySquare.objects.filter(
            box_daily_square=box_daily_square,
            box_daily_square__is_closed=False,
            review=False
        ).exclude(
            date=date.today()
        )
        now = datetime.now()
        context['exchange'] = get_object_or_none(
            Exchange,
            currency=office.country.currency,
            month__month=now.month,
        )
        today = datetime.today() - timedelta(hours=5)
        context['box'] = box_daily_square
        context['offices'] = offices
        context['office'] = office
        context['partners_list'] = partners
        context['dq_list'] = dq_list
        context['box_user'] = user
        context['users'] = users
        context['units'] = units
        context['today'] = today.strftime('%d/%m/%Y')
        context['past_mvments'] = past_mvments
        context['categories'] = Category.objects.all()
        context['movements'] = movements

        return context
