from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from cajas.users.models.employee import Employee

from cajas.inventory.models.brand import Brand
from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from ...models.units import Unit
from ...models.unitItems import UnitItems
from ..serializers.unit_serializer import UnitSerializer
from webclient.views.utils import get_object_or_none


User = get_user_model()


class UnitDetail(generics.RetrieveUpdateAPIView):
    """
    """

    serializer_class = UnitSerializer
    queryset = Unit.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication,)

    def update(self, request, *args, **kwargs):
        pk = kwargs['pk']
        print(request.POST)
        unit = Unit.objects.get(pk=pk)
        unit.name = request.data["name"]
        collector = None
        supervisor = None
        if 'supervisor' in request.data:
            supervisor = User.objects.get(pk=request.data['supervisor'])
        if 'collector' in request.data:
            collector = User.objects.get(pk=request.data['collector'])
        unit.collector = collector
        unit.supervisor = supervisor
        unit.save()

        if request.data["elemts"]:
            values = request.data["elemts"].split(",")
            for value in values:
                if "form[form]["+value+"][options]" in request.data:
                    option = request.data["form[form]["+value+"][options]"].split(",")
                    if option[1] == "delete":
                        item = UnitItems.objects.filter(pk=option[0]).update(
                            is_deleted=True,
                            observations=request.data["form[form]["+value+"][reason]"]
                        )
                        UnitItems.objects.create(
                            unit=unit,
                            name=request.data["form[form]["+value+"][name]"],
                            brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                            price=request.data["form[form]["+value+"][price]"]
                        )
                    if option[1] == "edit":
                        item = UnitItems.objects.filter(pk=option[0]).update(
                            name=request.data["form[form]["+value+"][name]"],
                            brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                            price=request.data["form[form]["+value+"][price]"]
                        )
                else:
                    UnitItems.objects.create(
                        unit=unit,
                        name=request.data["form[form]["+value+"][name]"],
                        brand=get_object_or_404(Brand, pk=request.data["form[form]["+value+"][brand]"]),
                        price=request.data["form[form]["+value+"][price]"]
                    )

        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
