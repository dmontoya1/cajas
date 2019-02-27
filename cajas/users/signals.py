from allauth.account.signals import user_logged_in, user_logged_out

from django.db.models.signals import post_save
from django.dispatch import receiver

from boxes.models.box_partner import BoxPartner
from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.auth_logs import AuthLogs
from cajas.users.models.partner import Partner

from webclient.views.get_ip import get_ip

from movement.views.movement_don_juan.movement_don_juan import MovementDonJuan


@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip = get_ip(request)

    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGIN
    )
    log.save()


@receiver(user_logged_out)
def after_user_logged_out(sender, request, user, **kwargs):
    ip = get_ip(request)

    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGOUT
    )
    log.save()


@receiver(post_save, sender=Partner)
def create_partner_box(sender, **kwargs):
    if kwargs.get('created'):
        instance = kwargs.get('instance')
        box = BoxPartner(
            partner=instance,
        )
        box.save()
