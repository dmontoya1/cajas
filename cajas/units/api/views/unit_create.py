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
        unit = Unit()
        unit.name = request.data["name"]
        unit.partner = get_object_or_404(Partner, user__pk=request.data["partner"])
        unit.collector = get_object_or_404(User, pk=request.data["collector"])
        unit.supervisor = get_object_or_404(User, pk=request.data["supervisor"])
        unit.save()
        for i in range(int(request.data['count'])):
            try:
                UnitItems.objects.create(
                    unit=unit,
                    name=request.data["form[form]["+str(i)+"][name]"],
                    brand=get_object_or_404(Brand, pk=request.data["form[form]["+str(i)+"][brand]"]),
                    price=request.data["form[form]["+str(i)+"][price]"]
                )
            except:
                pass
        return Response(
            'Se ha creado la cadena exitosamente.',
            status=status.HTTP_201_CREATED
        )