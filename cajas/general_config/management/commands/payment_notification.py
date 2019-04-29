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
        todayDate = datetime.date.today()
        secretaries = Employee.objects.filter(charge__name="Secretaria")
        if todayDate.day > 25:
            todayDate += datetime.timedelta(7)
        todayDate = todayDate.replace(day=1)
        if todayDate == datetime.date.today():
            for secretary in secretaries:
                email_manager.send_payment_notification(domain, secretary)
                self.stdout.write(self.style.SUCCESS(
                    'Enviar correo ;)')
                )
