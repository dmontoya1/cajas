
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.office.models.officeCountry import OfficeCountry
from cajas.webclient.views.get_ip import get_ip

from ...services.chains_manager import ChainManager

chain_manager = ChainManager()


class ChainPay(APIView):
    """
    """

    def post(self, request, format=None):
        data = request.data.copy()
        data['responsible'] = request.user
        data['ip'] = get_ip(request)
        data['office'] = OfficeCountry.objects.get(pk=request.session['office'])
        function_response = chain_manager.internal_chain_pay(data)
        print(function_response)
        if function_response:
            return Response(
                'Se ha creado el pago exitosamente',
                status=status.HTTP_201_CREATED
            )
        return Response(
            'No hay un socio para este usuario en esta oficina.',
            status=status.HTTP_204_NO_CONTENT
        )
