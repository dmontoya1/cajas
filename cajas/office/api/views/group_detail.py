from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication
from cajas.office.models.officeCountry import OfficeCountry
from cajas.users.models.employee import Employee
from cajas.users.models.group import Group
from cajas.users.models.group_employee import GroupEmployee

from ...api.serializer.group_employee_serializer import GroupEmployeeSerializer


class GroupDetail(generics.RetrieveUpdateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        adm = get_object_or_404(Group, pk=kwargs['pk'])
        supervisors = GroupEmployee.objects.filter(group=adm)
        quest = GroupEmployeeSerializer(supervisors, many=True)
        return Response(quest.data)

    def update(self, request, *args, **kwargs):
        office = OfficeCountry.objects.get(pk=request.data['office'])
        group = Group.objects.get(pk=request.data["admin"])
        group.office = office
        group.save()
        GroupEmployee.objects.filter(
            group=group,
        ).delete()
        for sup in request.POST.getlist("supervisors[]"):
            supervisor = Employee.objects.get(pk=sup)
            GroupEmployee.objects.create(
                group=group,
                supervisor=supervisor
            )
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
