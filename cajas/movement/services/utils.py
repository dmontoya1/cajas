
def get_related_movement_by_date_and_pk(model, box_name, box, date, pk):
    return model.objects.filter(**{
        box_name: box,
    }).filter(
        date__gte=date,
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
        print(movement.concept, movement.date, movement.balance)
        print("-------------------")
        if movement.movement_type == 'IN':
            movement.balance = balance + movement.value
            movement.save()
        else:
            movement.balance = balance - movement.value
            movement.save()
        balance = movement.balance
    box.balance = balance
    box.save()
