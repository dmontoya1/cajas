
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.concepts.models.concepts import Concept
from cajas.movement.services.don_juan_service import DonJuanManager
from cajas.movement.services.partner_service import MovementPartnerManager
from cajas.users.models.partner import Partner
from cajas.webclient.views.get_ip import get_ip

from ...models.units import Unit


class UnitSell(APIView):
    """ Endpoint para la venta de unidades
    """

    PROPERTIES = ['partner', 'unit', 'buyer_partner', 'total_price', 'price_items', 'unit_price']

    @staticmethod
    def __validate_data(self, data):
        if not all(property in data for property in self.PROPERTIES):
            raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def post(self, request, format=None):
        self.__validate_data(self, request.data)
        unit = Unit.objects.get(pk=request.data['unit'])
        seller_partner = Partner.objects.get(pk=request.data['partner'])
        buyer_partner = Partner.objects.get(pk=request.data['buyer_partner'])
        price = int(request.data['total_price'])
        concept = get_object_or_404(Concept, name='Compra de unidad')
        movement_partner_manager = MovementPartnerManager()
        don_juan_manager = DonJuanManager()

        unit.partner = buyer_partner
        unit.save()

        ip = get_ip(request)
        if seller_partner.code == 'DONJUAN':
            data_seller = {
                'box': BoxDonJuan.objects.get(office=seller_partner.office),
                'concept': concept.counterpart,
                'date': datetime.now(),
                'movement_type': 'IN',
                'value': price,
                'detail': 'Venta de unidad {} al socio {}. Precio inventario: ${} - Precio de venda+: ${}'.format(
                    unit.name,
                    seller_partner.get_full_name(),
                    request.data['price_items'],
                    request.data['unit_price']
                ),
                'responsible': request.user,
                'ip': ip,
            }
            don_juan_manager.create_movement(data_seller)
        else:
            data_seller = {
                'box': seller_partner.box,
                'concept': concept.counterpart,
                'date': datetime.now(),
                'movement_type': 'IN',
                'value': price,
                'detail': 'Venta de unidad {} al socio {}. Precio inventario: ${} - Precio de venda+: ${}'.format(
                    unit.name,
                    buyer_partner.get_full_name(),
                    request.data['price_items'],
                    request.data['unit_price']
                ),
                'responsible': request.user,
                'ip': ip,
            }
            movement_partner_manager.create_simple(data_seller)

        if buyer_partner.code == 'DONJUAN':
            data_buyer = {
                'box': BoxDonJuan.objects.get(office=seller_partner.office),
                'concept': concept,
                'date': datetime.now(),
                'movement_type': 'OUT',
                'value': price,
                'detail': 'Compra de unidad {} del socio {}. Precio inventario: ${} - Precio de venda+: ${}'.format(
                    unit.name,
                    seller_partner.get_full_name(),
                    request.data['price_items'],
                    request.data['unit_price']
                ),
                'responsible': request.user,
                'ip': ip,
            }
            don_juan_manager.create_movement(data_buyer)
        else:
            data_buyer = {
                'box': buyer_partner.box,
                'concept': concept,
                'date': datetime.now(),
                'movement_type': 'OUT',
                'value': price,
                'detail': 'Compra de unidad {} del socio {}. Precio inventario: ${} - Precio de venda+: ${}'.format(
                    unit.name,
                    seller_partner.get_full_name(),
                    request.data['price_items'],
                    request.data['unit_price']
                ),
                'responsible': request.user,
                'ip': ip,
            }
            movement_partner_manager.create_simple(data_buyer)

        seller_partner.buyer_unit_partner = buyer_partner
        seller_partner.save()
        return Response(
            'El movimiento se ha aprobado exitosamente. Se han creado los movimientos en las cajas correspondientes',
            status=status.HTTP_201_CREATED
        )
