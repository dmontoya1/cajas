
from django import template

from ..models.box_daily_square import BoxDailySquare

register = template.Library()


@register.simple_tag
def get_dq_box_balance(office, user):
    box, created = BoxDailySquare.objects.get_or_create(user=user, office=office)
    return box.balance


@register.simple_tag
def get_dq_box_id(office, user):
    box, created = BoxDailySquare.objects.get_or_create(user=user, office=office)
    return box.id


@register.simple_tag
def get_dq_box_is_close(office, user):
    box, created = BoxDailySquare.objects.get_or_create(user=user, office=office)
    return box.is_closed
