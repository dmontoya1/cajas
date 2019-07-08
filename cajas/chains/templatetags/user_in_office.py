
from django import template

register = template.Library()

from cajas.users.models.partner import Partner


@register.simple_tag
def user_in_office(user, office):
    try:
        partner = Partner.objects.get(user=user, office=office)
        if partner:
            return True
    except Partner.DoesNotExist:
        return False

