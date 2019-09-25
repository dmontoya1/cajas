
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept
from cajas.webclient.views.get_ip import get_ip

from ....services.don_juan_usd_service import DonJuanUSDManager
from ....services.don_juan_service import DonJuanManager


class MovementUSDCreate(APIView):

    def post(self, request, format=None):
        data = request.data
        box_don_juan = get_object_or_404(BoxDonJuanUSD, pk=data['box'])
        ip = get_ip(request)
        concept = get_object_or_404(Concept, pk=data['concept'])
        data_send = {
            'box': box_don_juan,
            'concept': concept,
            'date': data['date'],
            'detail': data['detail'],
            'movement_type': data['movement_type'],
            'responsible': request.user,
            'ip': ip,
        }
        don_juan_usd_manager = DonJuanUSDManager()
        don_juan_manager = DonJuanManager()
        if concept.name == 'Compra Dólares':
            data_send['value'] = data['buy_usd_value']
            don_juan_usd_manager.create_movement(data_send)
            if data['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            data_send_1 = {
                'box': get_object_or_404(BoxDonJuan, office__pk=data['office']),
                'concept': concept.counterpart,
                'date': data['date'],
                'movement_type': contrapart,
                'value': data['buy_value'],
                'detail': data['detail'],
                'responsible': request.user,
                'ip': ip,
            }
            don_juan_manager.create_movement(data_send_1)
        elif concept.name == 'Venta Dólares':
            data_send['value'] = data['sell_usd_value']
            don_juan_usd_manager.create_movement(data_send)
            if data['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            data_send_1 = {
                'box': get_object_or_404(BoxDonJuan, office__pk=data['office']),
                'concept': concept.counterpart,
                'date': data['date'],
                'movement_type': contrapart,
                'value': data['sell_value'],
                'detail': data['detail'],
                'responsible': request.user,
                'ip': ip,
            }
            don_juan_manager.create_movement(data_send_1)
        elif concept.name == 'Traslado entre cajas Colombia':
            data_send['value'] = data['value']
            don_juan_usd_manager.create_movement(data_send)
            if data['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            data_send_1 = {
                'concept': concept.counterpart,
                'date': data['date'],
                'movement_type': contrapart,
                'value': data['value_cop'],
                'detail': data['detail'],
                'responsible': request.user,
                'ip': ip,
            }
            don_juan_usd_manager.create_traslate_movement(data_send_1)
        else:
            data_send['value'] = data['value']
            don_juan_usd_manager.create_movement(data_send)

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
