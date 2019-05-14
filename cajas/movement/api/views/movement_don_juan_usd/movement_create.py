
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.boxes.models.box_don_juan import BoxDonJuan
from cajas.boxes.models.box_don_juan_usd import BoxDonJuanUSD
from cajas.concepts.models.concepts import Concept
from cajas.webclient.views.get_ip import get_ip
from ....models.movement_don_juan_usd import MovementDonJuanUsd
from ....models.movement_don_juan import MovementDonJuan


class MovementUSDCreate(APIView):

    def post(self, request, format=None):
        data = request.data
        concept = get_object_or_404(Concept, pk=data['concept'])
        if concept.name == 'Compra Dólares':
            MovementDonJuanUsd.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuanUSD, pk=data['box']),
                concept=concept,
                movement_type=data['movement_type'],
                value=data['buy_usd_value'],
                detail=data['detail'],
                date=data['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            if data['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            MovementDonJuan.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuan, office__pk=data['office']),
                concept=concept.counterpart,
                movement_type=contrapart,
                value=data['buy_value'],
                detail=data['detail'],
                date=data['date'],
                responsible=request.user,
                ip=get_ip(request)
            )

        elif concept.name == 'Venta Dólares':
            MovementDonJuanUsd.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuanUSD, pk=data['box']),
                concept=concept,
                movement_type=data['movement_type'],
                value=data['sell_usd_value'],
                detail=data['detail'],
                date=data['date'],
                responsible=request.user,
                ip=get_ip(request)
            )
            if data['movement_type'] == 'OUT':
                contrapart = 'IN'
            else:
                contrapart = 'OUT'
            MovementDonJuan.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuan, office__pk=data['office']),
                concept=concept.counterpart,
                movement_type=contrapart,
                value=data['sell_value'],
                detail=data['detail'],
                date=data['date'],
                responsible=request.user,
                ip=get_ip(request)
            )

        else:
            MovementDonJuanUsd.objects.create(
                box_don_juan=get_object_or_404(BoxDonJuanUSD, pk=data['box']),
                concept=concept,
                movement_type=data['movement_type'],
                value=data['value'],
                detail=data['detail'],
                date=data['date'],
                responsible=request.user,
                ip=get_ip(request)
            )

        return Response(
            'Se ha creado el movimiento exitosamente',
            status=status.HTTP_201_CREATED
        )
