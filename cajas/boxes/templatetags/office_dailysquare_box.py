
from django import template

from ..models.box_daily_square import BoxDailySquare

register = template.Library()


@register.simple_tag
def get_dq_box(office, user):
    box = BoxDailySquare.objects.get(user=user, office=office)
    return box.balance
