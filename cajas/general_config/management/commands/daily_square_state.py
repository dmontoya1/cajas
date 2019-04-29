from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from boxes.models.box_daily_square import BoxDailySquare
from core.services.email_service import EmailManager

User = get_user_model()
email_manager = EmailManager()


class Command(BaseCommand):
    help = 'it notifies if is there an open box'

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        daily_squares = User.objects.filter(is_daily_square=True)
        for user in daily_squares:
            if not user.related_daily_box.get().is_closed:
                email_manager.send_close_box_mail(domain, user.email)
                self.stdout.write(self.style.WARNING(
                    'Open daily square box "%s"' % user.related_daily_box.get())
                )
            else:
                BoxDailySquare.objects.filter(pk=user.related_daily_box.get().pk).update(is_closed=False)
                self.stdout.write(self.style.SUCCESS(
                    'Reseted daily square box "%s"' % user.related_daily_box.get())
                )
