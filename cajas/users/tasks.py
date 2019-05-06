import datetime
import logging

from django.contrib.sites.models import Site

from celery.schedules import crontab
from celery.task import periodic_task

from cajas.users.models.employee import Employee
from cajas.core.services.email_service import EmailManager


logger = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(minute=30, hour=3)),
    name="payment_notification"
)
def payment_notification():
    logger.info("payment notification execution")
    email_manager = EmailManager()
    domain = Site.objects.get_current().domain
    first_month_day = datetime.date.today()
    secretaries = Employee.objects.filter(charge__name="Secretaria")
    if first_month_day.day > 25:
        first_month_day += datetime.timedelta(7)
    first_month_day = first_month_day.replace(day=1)

    saturday_is_first_month_day = first_month_day.weekday() == 5
    sunday_is_first_month_day = first_month_day.weekday() == 6
    today_is_monday_if_first_is_saturday = datetime.date.today().day == 3
    today_is_monday_if_first_is_sunday = datetime.date.today().day == 2

    if (saturday_is_first_month_day and today_is_monday_if_first_is_saturday) or \
        (sunday_is_first_month_day and today_is_monday_if_first_is_sunday) or \
        (first_month_day == datetime.date.today()):
        for secretary in secretaries:
            email_manager.send_payment_notification(domain, secretary.user.email)
            logger.info('Enviar correo ;)')
