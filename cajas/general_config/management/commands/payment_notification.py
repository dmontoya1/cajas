import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from cajas.users.models.employee import Employee
from core.services.email_service import EmailManager

email_manager = EmailManager()


class Command(BaseCommand):
    help = 'It notifies at first day of the month'

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        first_month_day = datetime.date.today()
        secretaries = Employee.objects.filter(charge__name="Secretaria")
        if first_month_day.day > 25:
            first_month_day += datetime.timedelta(7)
        first_month_day = first_month_day.replace(day=1)

        if first_month_day.weekday() == 5 and datetime.date.today().day == 3:
            self.send_email(secretaries, domain, secretary.user.email)
        elif first_month_day.weekday() == 6 and datetime.date.today().day == 2:
            self.send_email(secretaries, domain, secretary.user.email)
        elif first_month_day == datetime.date.today():
            self.send_email(secretaries, domain, secretary.user.email)

    def send_email(self, secretaries, domain, email):
        for secretary in secretaries:
            email_manager.send_payment_notification(domain, secretary.user.email)
            self.stdout.write(self.style.SUCCESS(
                'Enviar correo ;)')
            )
