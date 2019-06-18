
import datetime
from django import template

from cajas.webclient.services.arqueo_service import ArqueoManager

register = template.Library()


@register.simple_tag
def get_office_arqueada(office):
    arqueo_manager = ArqueoManager()
    saturday = get_last_saturday()
    deficit = arqueo_manager.get_arqueo_by_office(office, saturday)
    return deficit


def get_last_saturday():
    today = datetime.date.today()
    today_day = (today.weekday() + 1) % 7
    saturday = today - datetime.timedelta(7 + today_day - 6)
    return saturday
