
import logging

logger = logging.getLogger(__name__)


def get_next_related_movement_by_date_and_pk(model, box_name, box, date_mv, pk):
    if len(model.objects.filter(**{box_name: box}).filter(date=date_mv, pk__gt=pk)) > 0:
        return model.objects.filter(**{box_name: box}).filter(
            date__gte=date_mv,
        ).exclude(date=date_mv, pk__lt=pk).order_by('date', 'pk')
    else:
        return model.objects.filter(**{box_name: box}).filter(
            date__gt=date_mv,
        ).order_by('date', 'pk')


def get_related_movement_by_date(model, box_name, box, date):
    return model.objects.filter(**{
        box_name: box,
    }).filter(
        date__gt=date,
    ).order_by('date', 'pk')


def update_movements_balance(movements, current_balance, box):
    balance = current_balance
    for movement in movements:
        if movement.movement_type == 'IN':
            movement.balance = balance + movement.value
            movement.save()
        else:
            movement.balance = balance - movement.value
            movement.save()
        balance = movement.balance
    box.balance = balance
    box.save()


def get_last_movement_on_delete(model, box_name, box, date_mv, pk):
    if len(model.objects.filter(**{box_name: box}).filter(date=date_mv, pk__lt=pk)) > 0:
        return model.objects.filter(**{box_name: box}).filter(
            date=date_mv,
            pk__lt=pk
        ).order_by('date', 'pk').last()
    else:
        return model.objects.filter(**{box_name: box}).filter(
            date__lt=date_mv,
        ).order_by('date', 'pk').last()


def delete_movement_by_box(current_movement, box, model, box_name):
    last_movement = get_last_movement_on_delete(
        model,
        box_name,
        box,
        current_movement.date,
        current_movement.pk
    )
    current_movement.delete()
    if last_movement:
        related_movements = get_next_related_movement_by_date_and_pk(
            model,
            box_name,
            box,
            last_movement.date,
            last_movement.pk
        )
        update_movements_balance(
            related_movements,
            last_movement.balance,
            box,
        )


def get_last_movement(model, box_name, box, date_mv,):
    if len(model.objects.filter(**{box_name: box}).filter(date=date_mv)) > 0:
        return model.objects.filter(**{box_name: box}).filter(date=date_mv).order_by('date', 'pk').last()
    else:
        return model.objects.filter(**{box_name: box}).filter(date__lt=date_mv).order_by('date', 'pk').last()


def update_movement_balance_on_create(last_movement, movement):
    try:
        last_balance = last_movement.balance
    except:
        last_balance = 0
    if movement.movement_type == 'IN':
        movement.balance = int(last_balance) + int(movement.value)
    else:
        movement.balance = int(last_balance) - int(movement.value)
    movement.save()


def update_all_movements_balance_on_create(model, box_name, box, date_mv, movement):
    related_movements = get_related_movement_by_date(
        model,
        box_name,
        box,
        date_mv,
    )
    update_movements_balance(
        related_movements,
        movement.balance,
        box
    )


def update_all_movement_balance_on_update(model, box_name, box, date_mv, pk, movement):
    related_movements = get_next_related_movement_by_date_and_pk(
        model,
        box_name,
        box,
        date_mv,
        pk
    )
    for mv in related_movements:
        print("RELATED")
        print(mv.date, "|", mv.pk, "|", mv.concept, "|", mv.value, "|", mv.balance)
    update_movements_balance(
        related_movements,
        movement.balance,
        box
    )


def update_movement_balance_full_box(model, box_name, box, date_mv, movement):
    related_movements = get_related_movement_by_date(
        model,
        box_name,
        box,
        date_mv,
    )
    update_movements_balance(
        related_movements,
        movement.balance,
        box
    )


def update_movement_type_value(movement_type, movement, value):
    if movement_type == 'IN':
        movement.balance += (int(value) * 2)
    else:
        movement.balance -= (int(value) * 2)
    movement.save()
    return movement


def update_movement_balance(movement, value):
    if movement.movement_type == 'IN':
        movement.balance -= movement.value
        movement.balance += int(value)
    else:
        movement.balance += movement.value
        movement.balance -= int(value)
    movement.save()
    return movement
