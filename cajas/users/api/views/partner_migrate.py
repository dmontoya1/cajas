
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.users.services.partner_service import PartnerManager
from cajas.webclient.views.get_ip import get_ip


class PartnerMigrate(APIView):

    def post(self, request):
        data = request.POST.copy()
        data['responsible'] = request.user
        data['ip'] = get_ip(request)
        partner_manager = PartnerManager()
        partner_manager.migrate_partner(data)

        return Response(
            'Se ha migrado el socio exitosamente',
            status=status.HTTP_201_CREATED
        )
