
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from cajas.users.models.partner import Partner
from office.models.office import Office
from ..models.chain import Chain
from ..models.chain_place import ChainPlace
from ..models.user_place import UserPlace

User = get_user_model()


class ChainManager(object):

    def chain_manager(self, data):
        chain = self.create_chain(data)
        self.create_chain_places(data, chain)

    def create_chain(self, data):
        office = get_object_or_404(Office, pk=int(data['office']))
        return Chain.objects.create(
            office=office,
            name=data['name'],
            places=data['places'],
            place_value=data['place_value'],
            chain_type=data['chain_type']
        )

    def create_chain_places(self, data, chain):
        places = int(data['places'])
        for i in range(1, places+1):
            place = ChainPlace.objects.create(
                chain=chain,
                name="Puesto {}".format(i),
                pay_date=data['pay_date_{}'.format(i)]
            )
            self.create_users_place(data, place, i)

    def create_users_place(self, data, place, i):
        counters = data['counters']
        for j in range(0, int(counters['counter_{}'.format(i)])):
            partner = get_object_or_404(Partner, pk=int(data['form[form][{}][partner_{}]'.format(j, i)]))
            user_place = UserPlace.objects.create(
                chain_place=place,
                user=partner.user,
                place_porcentaje=data['form[form][{}][place_porcentaje_{}]'.format(j, i)],
            )
