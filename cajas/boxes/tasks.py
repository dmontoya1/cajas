import logging

from celery.schedules import crontab
from celery.task import periodic_task

from django.contrib.auth import get_user_model


logger = logging.getLogger(__name__)


@periodic_task(
    run_every=(crontab(hour=8)),
    name="daily_square_state"
)
def daily_square_state():
    User = get_user_model()

    daily_squares = User.objects.filter(is_daily_square=True)
    for user in daily_squares:
        daily_box_user = user.related_daily_box.all()
        for box in daily_box_user:
            if not box.is_closed:
                logger.info(
                    'Open daily square box "%s"' % box
                )
            else:
                box.is_closed = False
                box.save()
                logger.info(
                    'Reseted daily square box "%s"' % box
                )
