
from datetime import date, timedelta
from django import template

register = template.Library()


@register.filter()
def three_last_days(a_date):
    today = date.today()-timedelta(days=3)
    if a_date >= today:
        return True
    return False
