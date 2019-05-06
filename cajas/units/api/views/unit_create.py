from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from cajas.inventory.models.brand import Brand
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.users.models.partner import Partner
from cajas.units.models.units import Unit
from cajas.webclient.views.utils import get_object_or_none

from ...models.unitItems import UnitItems


User = get_user_model()


class UnitCreate(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request, format=None):
        values = request.data["elemts"].split(",")
        unit = Unit.objects.create(
            name=request.data["name"],
            partner=get_object_or_404(Partner, pk=request.data["partner"]),
            collector=get_object_or_none(User, pk=request.POST.get('collector', None)),
            supervisor=get_object_or_none(User, pk=request.POST.get('supervisor', None)),
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
