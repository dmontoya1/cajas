
from django import template

from ..models.chain_place import ChainPlace

register = template.Library()


@register.simple_tag
def pay_per_month(place, month):
    chain_place = ChainPlace.objects.get(pk=place)
    pay = 0
    for u in chain_place.related_users.all():
        for p in u.related_payments.all():
            if p.date.month == month:
                pay += p.pay_value
    return int(pay)
