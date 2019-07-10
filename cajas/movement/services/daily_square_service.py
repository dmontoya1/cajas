
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Sum

from cajas.boxes.models import BoxDailySquare
from cajas.concepts.models.concepts import Concept
from cajas.concepts.services.stop_service import StopManager
from cajas.core.services.email_service import EmailManager
from cajas.users.models.user import User
from cajas.office.models.officeCountry import OfficeCountry
from cajas.units.models.units import Unit
from cajas.webclient.views.utils import get_object_or_none
from ..models import MovementDailySquare, MovementPartner, MovementDonJuan, MovementOffice, \
    MovementDonJuanUsd
from .utils import update_movements_balance, get_related_movement_by_date_and_pk, get_related_movement_by_date


class MovementDailySquareManager(object):

    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip',
                  'unit', 'user', 'office', 'loan', 'chain']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_movement(self, data):
        self.__validate_data(data)
        if len(MovementDailySquare.objects.filter(box_daily_square=data['box'], date=data['date'])) > 0:
            last_movement = MovementDailySquare.objects.filter(
                date=data['date'],
                box_daily_square=data['box'],
            ).order_by('date', 'pk').last()
        else:
            last_movement = MovementDailySquare.objects.filter(
                box_daily_square=data['box'],
                date__lt=data['date']
            ).order_by('date', 'pk').last()
        movement = MovementDailySquare.objects.create(
            box_daily_square=data['box'],
            concept=data['concept'],
            movement_type=data['movement_type'],
            value=data['value'],
            detail=data['detail'],
            date=data['date'],
            responsible=data['responsible'],
            ip=data['ip'],
            unit=data['unit'],
            user=data['user'],
            office=data['office'],
        )
        try:
            last_balance = last_movement.balance
        except:
            last_balance = 0
        print(last_balance)
        if movement.movement_type == MovementDailySquare.IN:
            movement.balance = int(last_balance) + int(movement.value)
        else:
            movement.balance = int(last_balance) - int(movement.value)
        movement.save()
        print(movement.balance)
        related_movements = get_related_movement_by_date(
            MovementDailySquare,
            'box_daily_square',
            data['box'],
            data['date'],
        )
        print(related_movements)
        update_movements_balance(related_movements, movement.balance, movement.box_daily_square)
        return movement

    def create_new_partner_movement(self, data):
        movement = MovementDailySquare.objects.create(
            box_daily_square=data['box'],
            concept=Concept.objects.get(name='Aporte personal socio'),
            movement_type='IN',
            value=data['value'],
            detail='Aporte personal {}'.format(data['partner']),
            date=datetime.now(),
            responsible=data['responsible'],
            ip=data['ip'],
        )
        return movement

    def get_user_value(self, data):
        month = datetime.now().month
        total = MovementDailySquare.objects.filter(
            box_daily_square=data['box'],
            concept=data['concept'],
            movement_type='OUT',
            date__month=month,
        ).aggregate(Sum('value'))
        if total['value__sum'] is None:
            total['value__sum'] = 0
        return total

    def get_out_movement_current_value_by_box_and_concept(self, box, concept):
        month = datetime.now().month
        total = MovementDailySquare.objects.filter(
            box_daily_square=box,
            concept=concept,
            movement_type='OUT',
            date__month=month,
        ).aggregate(Sum('value'))
        if total['value__sum'] is None:
            total['value__sum'] = 0
        return total

    def __get_movement_by_pk(self, pk):
        return MovementDailySquare.objects.filter(pk=pk)

    def __get_user_by_pk(self, pk):
        User = get_user_model()
        return User.objects.get(pk=pk)

    def __get_user_box_daily_square(self, user_id, office_slug):
        return BoxDailySquare.objects.get(user__pk=user_id, office__slug=office_slug)

    def __get_current_concept(self, pk):
        return Concept.objects.get(pk=pk)

    def __is_movement_type_updated(self, movement, movement_type):
        return movement.movement_type != movement_type

    def __is_money_delivery_and_target_has_changed(self, concept, movement, dq):
        if concept.name == 'Traslado de Efectivo entre Cuadres Diarios':
            if movement.user:
                return int(movement.user.pk) != int(dq)
            else:
                return True
        else:
            return False

    def __is_movement_value_updated(self, movement, value):
        return movement.value != value

    def __update_movement_type(self, data):
        current_movement = data['movement']
        self.__update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if current_movement.movement_don_juan:
            self.__update_movement_type_value(
                current_movement.movement_don_juan.movement_type,
                current_movement.movement_don_juan,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDonJuan,
                'box_don_juan',
                current_movement.movement_don_juan.box_don_juan,
                current_movement.movement_don_juan.date,
                current_movement.movement_don_juan.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )
        if current_movement.movement_don_juan_usd:
            self.__update_movement_type_value(
                current_movement.movement_don_juan_usd.movement_type,
                current_movement.movement_don_juan_usd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan_usd)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDonJuanUsd,
                'box_don_juan',
                current_movement.movement_don_juan_usd.box_don_juan,
                current_movement.movement_don_juan_usd.date,
                current_movement.movement_don_juan_usd.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )
        if current_movement.movement_partner:
            self.__update_movement_type_value(
                current_movement.movement_partner.movement_type,
                current_movement.movement_partner,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_partner)
            related_movements = get_related_movement_by_date_and_pk(
                MovementPartner,
                'box_partner',
                current_movement.movement_partner.box_partner,
                current_movement.movement_partner.date,
                current_movement.movement_partner.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )
        if current_movement.movement_office:
            self.__update_movement_type_value(
                current_movement.movement_office.movement_type,
                current_movement.movement_office,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_office)
            related_movements = get_related_movement_by_date_and_pk(
                MovementOffice,
                'box_office',
                current_movement.movement_office.box_office,
                current_movement.movement_office.date,
                current_movement.movement_office.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )
        if current_movement.movement_cd:
            self.__update_movement_type_value(
                current_movement.movement_cd.movement_type,
                current_movement.movement_cd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_cd)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDailySquare,
                'box_daily_square',
                current_movement.movement_cd.box_daily_square,
                current_movement.movement_cd.date,
                current_movement.movement_cd.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )

    def __update_movement_type_value(self, movement_type, movement, value):
        if movement_type == MovementDailySquare.IN:
            movement.balance += (int(value) * 2)
        else:
            movement.balance -= (int(value) * 2)
        movement.save()

    def update_counterpart_movement_type(self, movement):
        if movement.movement_type == movement.IN:
            movement.movement_type = movement.OUT
        else:
            movement.movement_type = movement.IN
        movement.save()

    def __update_new_target_user_on_delivery_money(self, data):
        current_movement = self.__get_movement_by_pk(data['pk']).first()
        if current_movement.movement_cd:
            current_movement.movement_cd.delete()
        data['box'] = self.__get_user_box_daily_square(data['dq'], data['office_slug'])
        data['concept'] = self.__get_current_concept(data['concept']).counterpart
        data['unit'] = None
        data['user'] = self.__get_user_by_pk(data['dq'])
        data['loan'] = None
        data['chain'] = None
        data['office'] = get_object_or_none(OfficeCountry, pk=data.get('office', None))
        if current_movement.movement_type == 'OUT':
            data['movement_type'] = 'IN'
        else:
            data['movement_type'] = 'OUT'
        return self.create_movement(data)

    def __update_value(self, data):
        current_movement = data['movement']
        self.__update_movement_balance(current_movement, data['value'])
        if current_movement.movement_don_juan:
            self.__update_movement_balance(
                current_movement.movement_don_juan,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDonJuan,
                'box_don_juan',
                current_movement.movement_don_juan.box_don_juan,
                current_movement.movement_don_juan.date,
                current_movement.movement_don_juan.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan.balance,
                current_movement.movement_don_juan.box_don_juan
            )
        if current_movement.movement_don_juan_usd:
            self.__update_movement_balance(
                current_movement.movement_don_juan_usd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan_usd)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDonJuanUsd,
                'box_don_juan',
                current_movement.movement_don_juan_usd.box_don_juan,
                current_movement.movement_don_juan_usd.date,
                current_movement.movement_don_juan_usd.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_don_juan_usd.balance,
                current_movement.movement_don_juan_usd.box_don_juan_usd
            )
        if current_movement.movement_partner:
            self.__update_movement_balance(
                current_movement.movement_partner,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_partner)
            related_movements = get_related_movement_by_date_and_pk(
                MovementPartner,
                'box_partner',
                current_movement.movement_partner.box_partner,
                current_movement.movement_partner.date,
                current_movement.movement_partner.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_partner.balance,
                current_movement.movement_partner.box_partner
            )
        if current_movement.movement_office:
            self.__update_movement_balance(
                current_movement.movement_office,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_office)
            related_movements = get_related_movement_by_date_and_pk(
                MovementOffice,
                'box_office',
                current_movement.movement_office.box_office,
                current_movement.movement_office.date,
                current_movement.movement_office.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_office.balance,
                current_movement.movement_office.box_office
            )
        if current_movement.movement_cd:
            self.__update_movement_balance(
                current_movement.movement_cd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_cd)
            related_movements = get_related_movement_by_date_and_pk(
                MovementDailySquare,
                'box_daily_square',
                current_movement.movement_cd.box_daily_square,
                current_movement.movement_cd.date,
                current_movement.movement_cd.pk
            )
            update_movements_balance(
                related_movements,
                current_movement.movement_cd.balance,
                current_movement.movement_cd.box_daily_square
            )

    def __update_movement_balance(self, movement, value):
        if movement.movement_type == MovementDailySquare.IN:
            movement.balance -= movement.value
            movement.balance += int(value)
        else:
            movement.balance += movement.value
            movement.balance -= int(value)
        movement.save()

    def update_counterpart_movement_value(self, movement, value):
        movement.value = value
        movement.save()

    def __delete_related_movement(self, movement):
        if movement.movement_don_juan:
            movement_don_juan = movement.movement_don_juan
            movement_don_juan.delete()
        if movement.movement_don_juan_usd:
            movement_don_juan_usd = movement.movement_don_juan_usd
            movement_don_juan_usd.delete()
        if movement.movement_partner:
            movement_partner = movement.movement_partner
            movement_partner.delete()
        if movement.movement_cd:
            movement_cd = movement.movement_cd
            movement_cd.delete()

    def update_daily_square_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        current_user_box_daily_square = self.__get_user_box_daily_square(data['user_id'], data['office_slug'])
        current_concept = self.__get_current_concept(data['concept'])
        user = data.get('dq', None)
        current_user = get_object_or_none(User, pk=data.get('user', None))
        object_data = dict()
        object_data['box_daily_square'] = current_user_box_daily_square
        object_data['concept'] = current_concept
        object_data['value'] = data['value']
        object_data['movement_type'] = data['movement_type']
        object_data['detail'] = data['detail']
        object_data['date'] = data['date']
        object_data['user'] = user
        object_data['office'] = get_object_or_none(OfficeCountry, pk=data.get('office', None))
        object_data['unit'] = get_object_or_none(Unit, pk=data.get('unit', None))
        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            data['movement'] = current_movement
            data['box'] = current_user_box_daily_square
            self.__update_movement_type(data)
        if self.__is_movement_value_updated(current_movement, data['value']):
            data['movement'] = current_movement
            data['box'] = current_user_box_daily_square
            self.__update_value(data)
        if user and self.__is_money_delivery_and_target_has_changed(current_concept, current_movement, user):
            movement_dq = self.__update_new_target_user_on_delivery_money(data)
            object_data['movement_cd'] = movement_dq
        if current_user is not None:
            stop_manager = StopManager(current_user)
            if stop_manager.user_has_tops_for_concept(current_concept):
                user_movements_top_value = stop_manager.get_user_movements_top_value_by_concept(current_concept)

                user_movements_current_value = self.get_out_movement_current_value_by_box_and_concept(
                    current_user_box_daily_square,
                    current_concept
                )
                informative_value = stop_manager.get_informative_user_top_value_movements_by_concept(current_concept)
                if informative_value != 0 and informative_value <= (user_movements_current_value + int(data['value'])):
                    email_manager = EmailManager()
                    email_manager.send_informative_top_notification(current_user, current_concept)
                if user_movements_top_value >= (user_movements_current_value + data['value']):
                    current_movement_daily_square.update(**object_data)
            else:
                raise Exception('user has exceed limit')
        else:
            current_movement_daily_square.update(**object_data)
        current_movement = MovementDailySquare.objects.get(pk=data['pk'])
        related_movements = get_related_movement_by_date_and_pk(
            MovementDailySquare,
            'box_daily_square',
            current_user_box_daily_square,
            current_movement.date,
            current_movement.pk
        )
        update_movements_balance(
            related_movements,
            current_movement.balance,
            current_user_box_daily_square
        )

    def delete_daily_square_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        self.__delete_related_movement(current_movement)
        current_movement.delete()
