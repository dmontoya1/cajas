from datetime import datetime, timedelta

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
from .utils import update_movements_balance, get_next_related_movement_by_date_and_pk, \
    update_movement_balance_on_create, delete_movement_by_box, get_last_movement, \
    update_all_movements_balance_on_create, update_all_movement_balance_on_update, update_movement_type_value, \
    update_movement_balance, update_movement_balance_full_box


class MovementDailySquareManager(object):
    PROPERTIES = ['box', 'concept', 'movement_type', 'value', 'detail', 'date', 'responsible', 'ip',
                  'unit', 'user', 'office', 'loan', 'chain']

    def __validate_data(self, data):
        for field in self.PROPERTIES:
            if field not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(field))

    def create_movement(self, data):
        self.__validate_data(data)
        last_movement = get_last_movement(MovementDailySquare, 'box_daily_square', data['box'], data['date'])
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
            if data['lender']:
                movement.temp_employee = data['lender']
        except:
            pass
        update_movement_balance_on_create(last_movement, movement)
        update_all_movements_balance_on_create(
            MovementDailySquare,
            'box_daily_square',
            data['box'],
            data['date'],
            movement
        )
        return movement

    def create_new_partner_movement(self, data):
        data_send = data.copy()
        data_send['concept'] = Concept.objects.get(name='Aporte personal socio')
        data_send['movement_type'] = 'IN'
        data_send['detail'] = 'Aporte personal {}'.format(data['partner'])
        data_send['date'] = datetime.now()
        data_send['unit'] = None
        data_send['user'] = None
        data_send['office'] = None
        data_send['loan'] = None
        data_send['chain'] = None
        return self.create_movement(data_send)

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

    def __is_date_updated(self, movement, new_date):
        return movement.date != new_date

    def __is_money_delivery_and_target_has_changed(self, concept, movement, dq):
        if concept.name == 'Traslado de Efectivo entre Cuadres Diarios':
            if movement.user:
                return int(movement.user.pk) != int(dq)
            else:
                return True
        else:
            return False

    def __is_movement_value_updated(self, movement, value):
        return int(movement.value) != int(value)

    def __update_movement_type(self, data):
        current_movement = data['movement']
        update_movement_type_value(data['movement_type'], current_movement, data['value'])
        if current_movement.movement_don_juan:
            update_movement_type_value(
                current_movement.movement_don_juan.movement_type,
                current_movement.movement_don_juan,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan)
            first_movement = MovementDonJuan.objects.filter(
                box_don_juan=current_movement.movement_don_juan.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuan,
                'box_don_juan',
                current_movement.movement_don_juan.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_don_juan_usd:
            update_movement_type_value(
                current_movement.movement_don_juan_usd.movement_type,
                current_movement.movement_don_juan_usd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_don_juan_usd)
            first_movement = MovementDonJuanUsd.objects.filter(
                box_don_juan=current_movement.movement_don_juan_usd.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuanUsd,
                'box_don_juan',
                current_movement.movement_don_juan_usd.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_partner:
            update_movement_type_value(
                current_movement.movement_partner.movement_type,
                current_movement.movement_partner,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_partner)
            first_movement = MovementPartner.objects.filter(
                box_partner=current_movement.movement_partner.box_partner
            ).last()
            update_movement_balance_full_box(
                MovementPartner,
                'box_partner',
                current_movement.movement_partner.box_partner,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_office:
            update_movement_type_value(
                current_movement.movement_office.movement_type,
                current_movement.movement_office,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_office)
            first_movement = MovementOffice.objects.filter(
                box_daily_square=current_movement.movement_office.box_office
            ).last()
            update_movement_balance_full_box(
                MovementOffice,
                'box_office',
                current_movement.movement_office.box_office,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_cd:
            update_movement_type_value(
                current_movement.movement_cd.movement_type,
                current_movement.movement_cd,
                data['value']
            )
            self.update_counterpart_movement_type(current_movement.movement_cd)
            first_movement = MovementDailySquare.objects.filter(
                box_daily_square=current_movement.movement_cd.box_daily_square
            ).last()
            update_movement_balance_full_box(
                MovementDailySquare,
                'box_daily_square',
                current_movement.movement_cd.box_daily_square,
                first_movement.date,
                first_movement
            )

    def update_counterpart_movement_type(self, movement):
        if movement.movement_type == movement.IN:
            movement.movement_type = movement.OUT
        else:
            movement.movement_type = movement.IN
        movement.save()

    def update_movement_value(self, movement, value):
        movement.value = value
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
        update_movement_balance(current_movement, data['value'])
        if current_movement.movement_don_juan:
            update_movement_balance(
                current_movement.movement_don_juan,
                data['value']
            )
            self.update_movement_value(current_movement.movement_don_juan, data['value'])
            first_movement = MovementDonJuan.objects.filter(
                box_don_juan=current_movement.movement_don_juan.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuan,
                'box_don_juan',
                current_movement.movement_don_juan.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_don_juan_usd:
            update_movement_balance(
                current_movement.movement_don_juan_usd,
                data['value']
            )
            self.update_movement_value(current_movement.movement_don_juan_usd, data['value'])
            first_movement = MovementDonJuanUsd.objects.filter(
                box_don_juan=current_movement.movement_don_juan_usd.box_don_juan
            ).last()
            update_movement_balance_full_box(
                MovementDonJuanUsd,
                'box_don_juan',
                current_movement.movement_don_juan_usd.box_don_juan,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_partner:
            update_movement_balance(
                current_movement.movement_partner,
                data['value']
            )
            self.update_movement_value(current_movement.movement_partner, data['value'])
            first_movement = MovementPartner.objects.filter(
                box_partner=current_movement.movement_partner.box_partner
            ).last()
            update_movement_balance_full_box(
                MovementPartner,
                'box_partner',
                current_movement.movement_partner.box_partner,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_office:
            update_movement_balance(
                current_movement.movement_office,
                data['value']
            )
            self.update_movement_value(current_movement.movement_office, data['value'])
            first_movement = MovementOffice.objects.filter(
                box_daily_square= current_movement.movement_office.box_office
            ).last()
            update_movement_balance_full_box(
                MovementOffice,
                'box_office',
                current_movement.movement_office.box_office,
                first_movement.date,
                first_movement
            )
        if current_movement.movement_cd:
            update_movement_balance(
                current_movement.movement_cd,
                data['value']
            )
            self.update_movement_value(current_movement.movement_cd, data['value'])
            first_movement = MovementDailySquare.objects.filter(
                box_daily_square=current_movement.movement_cd.box_daily_square
            ).last()
            update_movement_balance_full_box(
                MovementDailySquare,
                'box_daily_square',
                current_movement.movement_cd.box_daily_square,
                first_movement.date,
                first_movement
            )

    def __delete_related_movement(self, movement):
        if movement.movement_don_juan:
            delete_movement_by_box(
                movement.movement_don_juan,
                MovementDonJuan,
                movement.movement_don_juan.box_don_juan,
                'box_don_juan'
            )
        if movement.movement_don_juan_usd:
            delete_movement_by_box(
                movement.movement_don_juan_usd,
                movement.movement_don_juan_usd.box_don_juan,
                MovementDonJuanUsd,
                'box_don_juan_usd'
            )
        if movement.movement_partner:
            delete_movement_by_box(
                movement.movement_partner,
                movement.movement_partner.box_partner,
                MovementPartner,
                'box_partner'
            )
        if movement.movement_cd:
            delete_movement_by_box(
                movement.movement_cd,
                movement.movement_cd.box_daily_square,
                MovementDailySquare,
                'box_daily_square'
            )

    def __is_movement_date_update(self, movement, new_date):
        return movement.date != new_date

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
        data['movement'] = current_movement
        data['box'] = current_user_box_daily_square
        if self.__is_movement_type_updated(current_movement, data['movement_type']):
            self.__update_movement_type(data)
        if self.__is_movement_value_updated(current_movement, data['value']):
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
        all_movements = current_user_box_daily_square.movements.order_by('date', 'pk')
        update_movements_balance(
            all_movements,
            0,
            current_user_box_daily_square
        )
        # update_all_movement_balance_on_update(
        #     MovementDailySquare,
        #     'box_daily_square',
        #     current_user_box_daily_square,
        #     data['date'],
        #     current_movement.pk,
        #     current_movement
        # )
        if self.__is_movement_date_update(current_movement, data['date']):
            all_movements = current_user_box_daily_square.movements.order_by('date', 'pk')
            update_movements_balance(
                all_movements,
                0,
                current_user_box_daily_square
            )

    def delete_daily_square_movement(self, data):
        current_movement_daily_square = self.__get_movement_by_pk(data['pk'])
        current_movement = current_movement_daily_square.first()
        self.__delete_related_movement(current_movement)
        delete_movement_by_box(
            current_movement,
            current_movement.box_daily_square,
            MovementDailySquare,
            'box_daily_square'
        )
