
from cajas.webclient.views.utils import get_object_or_none
from ..models.stops import Stop
from cajas.users.models import Employee


class StopManager(object):

    def __init__(self, user):
        self.user = user

    def get_user_movements_top_value_by_concept(self, concept):
        stop_user = self.get_user_stop(concept)
        stop_charge = self.get_charge_stop(concept)
        stop_user, stop_charge = self.get_non_informative_stop_params(stop_user, stop_charge)
        stop_value = self.get_stop_value(stop_user, stop_charge)
        return stop_value

    def get_informative_user_top_value_movements_by_concept(self, concept):
        stop_user = self.get_user_stop(concept)
        stop_charge = self.get_charge_stop(concept)
        informative_stop_user, informative_stop_charge = self.get_informative_stop_params(stop_user, stop_charge)
        stop_value = self.get_stop_value(informative_stop_user, informative_stop_charge)
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
        return Stop.objects.filter(
            concept=concept,
            user=self.user
        )

    def get_charge_stop(self, concept):
        try:
            return Stop.objects.filter(
                concept=concept,
                charge=self.user.employee.get().charge
            )
        except:
            return None

    def get_informative_stop(self, stops):
        if stops is not None:
            for stop in stops:
                if stop.is_informative:
                    return stop

    def get_non_informative_stop(self, stops):
        if stops is not None:
            for stop in stops:
                if not stop.is_informative:
                    return stop

    def get_non_informative_stop_params(self, stop_user, stop_charge):
        stop_user = self.get_non_informative_stop(stop_user)
        stop_charge = self.get_non_informative_stop(stop_charge)
        return stop_user, stop_charge

    def get_informative_stop_params(self, stop_user, stop_charge):
        stop_user = self.get_informative_stop(stop_user)
        stop_charge = self.get_informative_stop(stop_charge)
        return stop_user, stop_charge
