
from django.db.models import Sum, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from cajas.boxes.models.box_partner import BoxPartner
from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.office.models.officeCountry import OfficeCountry


class ArcRequest(LoginRequiredMixin, TemplateView):
    """
    """

    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'webclient/arc_request.html'

    def get_context_data(self, **kwargs):
        context = super(ArcRequest, self).get_context_data(**kwargs)
        office = get_object_or_404(OfficeCountry, pk=self.request.session['office'])
        start_date = self.request.GET.get('date_start', None)
        end_date = self.request.GET.get('date_end', None)
        box_office = office.box
        box_donjuan = BoxDonJuan.objects.get(office=office)
        box_partners = BoxPartner.objects.filter(partner__office=office, is_active=True)
        box_daily = BoxDailySquare.objects.filter(office=office, user__is_daily_square=True)
        dq_total = 0
        partner_sum = 0
        data = dict()
        partners_list = dict()
        dailys_list = dict()
        total_office = 0
        total_don_juan = 0
        if start_date and end_date:
            movements_office = box_office.movements.filter(
                date__lte=end_date,
            )
            for mv in movements_office:
                if mv.movement_type == 'IN':
                    total_office += mv.value
                else:
                    total_office -= mv.value
            data['office'] = total_office
            movements_don_juan = box_donjuan.movements.filter(
                date__lte=end_date,
            )
            for mv in movements_don_juan:
                if mv.movement_type == 'IN':
                    total_don_juan += mv.value
                else:
                    total_don_juan -= mv.value
            data['don_juan'] = total_don_juan
            for box in box_partners:
                total_partner = 0
                movements = box.movements.filter(
                    date__lte=end_date,
                )
                for mv in movements:
                    if mv.movement_type == 'IN':
                        total_partner += mv.value
                    else:
                        total_partner -= mv.value
                partners_list[box.partner] = total_partner
                partner_sum += total_partner
            for box in box_daily:
                total_daily = 0
                movements = box.movements.filter(
                    Q(date__lte=end_date) &
                    ~Q(status='DE')
                )
                for mv in movements:
                    if mv.movement_type == 'IN':
                        total_daily += mv.value
                    else:
                        total_daily -= mv.value
                dailys_list[box.user.get_full_name()] = total_daily
                dq_total += total_daily
        else:
            total_don_juan = box_donjuan.balance
            total_office = box_office.balance
            data['office'] = total_office
            data['don_juan'] = total_don_juan
            for box in box_partners:
                partners_list[box.partner] = box.balance
            for box in box_daily:
                dailys_list[box.user.get_full_name()] = box.balance
            box_partners_total = box_partners.aggregate(Sum('balance'))
            box_daily_total = box_daily.aggregate(Sum('balance'))
            if box_daily_total['balance__sum'] is not None:
                dq_total = box_daily_total['balance__sum']
            if box_partners_total['balance__sum'] is not None:
                partner_sum = box_partners_total['balance__sum']

        data['partners'] = partners_list
        data['dailys'] = dailys_list

        partner_total = partner_sum + total_office + total_don_juan
        deficit = dq_total - partner_total
        context['data'] = data
        context['office'] = office
        context['box_donjuan'] = box_donjuan
        context['box_office'] = box_office
        context['box_daily_total'] = dq_total
        context['partner_total'] = partner_total
        context['deficit'] = deficit
        return context
