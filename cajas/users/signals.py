from allauth.account.signals import user_logged_in, user_logged_out

from django.db.models.signals import post_save
from django.dispatch import receiver

from boxes.models.box_partner import BoxPartner
from boxes.models.box_daily_square import BoxDailySquare
from cajas.users.models.auth_logs import AuthLogs
from cajas.users.models.partner import Partner


@receiver(user_logged_in)
def after_user_logged_in(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    log = AuthLogs(
        ip=ip,
        user=user,
        action=AuthLogs.LOGIN
    )
    log.save()


@receiver(user_logged_out)
def after_user_logged_out(sender, request, user, **kwargs):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

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
        if instance.is_daily_square:
            if BoxDailySquare.objects.get(user=instance.user):
                box_daily = BoxDailySquare.objects.get(user=instance.user)
            else:
                box_daily = None
            if not box_daily:
                box1 = BoxDailySquare(
                    user=instance.user
                )
                box1.save()
