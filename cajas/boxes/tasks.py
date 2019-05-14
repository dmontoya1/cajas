import logging

from celery.schedules import crontab
from celery.task import periodic_task

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site

from cajas.boxes.models.box_daily_square import BoxDailySquare
from cajas.core.services.email_service import EmailManager


logger = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(hour=8)),
    name="daily_square_state"
)
def daily_square_state():
    User = get_user_model()
    email_manager = EmailManager()

    domain = Site.objects.get_current().domain
    daily_squares = User.objects.filter(is_daily_square=True)
    for user in daily_squares:
        daily_box_user = user.related_daily_box.all()
        for box in daily_box_user:
            if not box.is_closed:
                logger.info(
                    'Open daily square box "%s"' % box
                )
            else:
                BoxDailySquare.objects.filter(pk=user.related_daily_box.get().pk).update(is_closed=False)
                logger.info(
                    'Reseted daily square box "%s"' % box
                )
