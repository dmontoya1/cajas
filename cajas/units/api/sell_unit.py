
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from cajas.users.models.partner import Partner
from concepts.models.concepts import Concept
from movement.views.movement_partner.movement_partner_handler import MovementPartnerHandler
from webclient.views.get_ip import get_ip
from ..models.units import Unit


class UnitSell(APIView):
    """ Api para la venta de unidades
    """

    PROPERTIES = ['partner', 'unit', 'buyer_partner', 'total_price', 'price_items', 'unit_price']

    @staticmethod
    def __validate_data(self, data):
        for property in self.PROPERTIES:
            if property not in data:
                raise Exception('la propiedad {} no se encuentra en los datos'.format(property))

    def post(self, request, format=None):
        self.__validate_data(self, request.data)
        unit = Unit.objects.get(pk=request.data['unit'])
        seller_partner = Partner.objects.get(pk=request.data['partner'])
        buyer_partner = Partner.objects.get(pk=request.data['buyer_partner'])
        price = int(request.data['total_price'])
        concept = get_object_or_404(Concept, name='Compra de unidad')

        unit.partner = buyer_partner
        unit.save()

        ip = get_ip(request)
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
        movement_seller = MovementPartnerHandler.create_simple(data_seller)
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
        movement_seller = MovementPartnerHandler.create_simple(data_buyer)

        return Response(
            'El movimiento se ha aprobado exitosamente. Se han creado los movimientos en las cajas correspondientes',
            status=status.HTTP_201_CREATED
        )
