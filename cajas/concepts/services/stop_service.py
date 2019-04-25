
from webclient.views.utils import get_object_or_none
from ..models.stops import Stop
from cajas.users.models import Employee


class StopManager(object):

    def __init__(self, user):
        self.user = user

    def get_user_movements_top_value_by_concept(self, concept):
        stop_user = self.get_user_stop(concept)
        stop_charge = self.get_charge_stop(concept)
        stop_value = self.get_stop_value(stop_user, stop_charge)
        return stop_value

    def user_has_tops_for_concept(self, concept):
        return self.get_user_movements_top_value_by_concept(concept) != 0

    def get_stop_value(self, stop_user, stop_charge):
        if stop_user:
            if stop_charge:
                if stop_user.value > stop_charge.value:
                    stop_value = stop_user.value
                else:
                    stop_value = stop_charge.value
            else:
                stop_value = stop_user.value
        elif stop_charge:
            stop_value = stop_charge.value
        else:
            stop_value = 0

        return stop_value

    def get_user_stop(self, concept):
        return get_object_or_none(
            Stop,
            concept=concept,
            user=self.user
        )

    def get_charge_stop(self, concept):
        try:
            return get_object_or_none(
                Stop,
                concept=concept,
                charge=self.user.employee.get().charge
            )
        except:
            return None
