from rest_framework.views import APIView
from rest_framework import generics

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from api.CsrfExempt import CsrfExemptSessionAuthentication

from inventory.models.brand import Brand
from cajas.users.models.employee import Employee

from ...serializers.movement_daily_square_request_item_serializer import MovementDailySquareRequestItemSerializer
from ....models.movement_daily_square_request_item import MovementDailySquareRequestItem
from ....models.movement_daily_square import MovementDailySquare


class DailySquareRequestItemDetail(generics.RetrieveUpdateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        movement = get_object_or_404(MovementDailySquare, pk=kwargs['pk'])
        request_item = MovementDailySquareRequestItem.objects.filter(movement=movement)
        quest = MovementDailySquareRequestItemSerializer(request_item, many=True)
        return Response(quest.data)

    def update(self, request, *args, **kwargs):
        print("asda", request.data)
        if request.data["elemts"] == '':
            return Response(
                'No se actualizó el inventario de unidad',
                status=status.HTTP_204_NO_CONTENT
            )
        movement = get_object_or_404(MovementDailySquare, pk=kwargs['pk'])
        request_item = MovementDailySquareRequestItem.objects.filter(movement=movement).delete()
        values = request.data["elemts"].split(",")
        for value in values:
            MovementDailySquareRequestItem.objects.create(
                movement=movement,
                name=request.data["form[form]["+value+"][name]"],
                brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                price=request.data["form[form]["+value+"][price]"]
            )
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
