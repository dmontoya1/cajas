from rest_framework.views import APIView
from rest_framework import generics

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from api.CsrfExempt import CsrfExemptSessionAuthentication

from cajas.users.models.employee import Employee
from cajas.users.models.group import Group
from cajas.users.models.group_employee import GroupEmployee
from ..serializer.group_employee_serializer import GroupEmployeeSerializer


class GroupDetail(generics.RetrieveUpdateAPIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        adm = get_object_or_404(Group, pk=kwargs['pk'])
        supervisors = GroupEmployee.objects.filter(group=adm)
        quest = GroupEmployeeSerializer(supervisors, many=True)
        return Response(quest.data)

    def update(self, request, *args, **kwargs):
        admin = Group.objects.get(pk=request.data["admin"])
        reset = GroupEmployee.objects.filter(
            group=admin,
        ).delete()
        for sup in request.POST.getlist("supervisors[]"):
            supervisor = Employee.objects.get(pk=sup)
            group = GroupEmployee.objects.create(
                group=admin,
                supervisor=supervisor
            )
        return Response(
            'El item se ha actualizado correctamente',
            status=status.HTTP_200_OK
        )
