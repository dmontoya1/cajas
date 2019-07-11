
def get_next_related_movement_by_date_and_pk(model, box_name, box, date_mv, pk):
    return model.objects.filter(**{
        box_name: box,
    }).filter(
        date__gte=date_mv,
        pk__gt=pk
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
            box_daily_square=box,
            pk__lt=pk
        ).order_by('date', 'pk').last()
    else:
        return model.objects.filter(**{box_name: box}).filter(
            box_daily_square=box,
            date__lt=date_mv,
        ).order_by('date', 'pk').last()


def delete_movement_by_box(current_movement, model, box_name):
    last_movement = get_last_movement_on_delete(
        model,
        box_name,
        current_movement.box_daily_square,
        current_movement.date,
        current_movement.pk
    )
    current_movement.delete()
    related_movements = get_next_related_movement_by_date_and_pk(
        model,
        box_name,
        last_movement.box_daily_square,
        last_movement.date,
        last_movement.pk
    )
    update_movements_balance(
        related_movements,
        last_movement.balance,
        last_movement.box_daily_square,
    )
