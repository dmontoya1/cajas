
from django.db.models import Q

from cajas.boxes.models.box_partner import BoxPartner
from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.boxes.models.box_don_juan import BoxDonJuan


class ArqueoManager(object):
    """
    """

    def get_arqueo_by_office(self, office, end_date):
        box_office = office.box
        box_donjuan = BoxDonJuan.objects.get(office=office)
        box_partners = BoxPartner.objects.filter(partner__office=office, is_active=True)
        box_daily = BoxDailySquare.objects.filter(office=office, user__is_daily_square=True)
        dq_total = 0
        partner_sum = 0
        total_office = 0
        total_don_juan = 0
        if end_date:
            movements_office = box_office.movements.filter(
                date__lte=end_date,
            )
            for mv in movements_office:
                if mv.movement_type == 'IN':
                    total_office += mv.value
                else:
                    total_office -= mv.value
            movements_don_juan = box_donjuan.movements.filter(
                date__lte=end_date,
            )
            for mv in movements_don_juan:
                if mv.movement_type == 'IN':
                    total_don_juan += mv.value
                else:
                    total_don_juan -= mv.value
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
                dq_total += total_daily

        partner_total = partner_sum + total_office + total_don_juan
        deficit = dq_total - partner_total
        return deficit
