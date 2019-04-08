from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from inventory.models.brand import Brand
from api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.users.models.partner import Partner
from units.models.units import Unit
from ...models.unitItems import UnitItems


User = get_user_model()


class UnitCreate(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        values = request.data["elemts"].split(",")
        unit = Unit.objects.create(
            name=request.data["name"],
            partner=get_object_or_404(Partner, pk=request.data["partner"]),
            collector=get_object_or_404(User, pk=request.data["collector"]),
            supervisor=get_object_or_404(User, pk=request.data["supervisor"])
        )
        for value in values:
            UnitItems.objects.create(
                unit=unit,
                name=request.data["form[form]["+value+"][name]"],
                brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                price=request.data["form[form]["+value+"][price]"]
            )
        return Response(
            'La unidad se ha creado exitosamente.',
            status=status.HTTP_201_CREATED
        )
