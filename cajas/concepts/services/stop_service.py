
from webclient.views.utils import get_object_or_none
from ..models.stops import Stop


class StopManager(object):

    def validate_stop(self, data):
        stop_user = self.get_user_stop(data)
        stop_charge = self.get_charge_stop(data)
        stop_value = self.get_stop_value(stop_user, stop_charge)
        return stop_value

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

    def get_user_stop(self, data):
        return get_object_or_none(
            Stop,
            concept=data['concept'],
            user=data['_user']
        )

    def get_charge_stop(self, data):
        try:
            return get_object_or_none(
                Stop,
                concept=data['concept'],
                charge=data['_user'].employee.get().charge
            )
        except:
            return None
