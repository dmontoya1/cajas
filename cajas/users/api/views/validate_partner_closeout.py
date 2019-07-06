
import logging

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from cajas.users.models.partner import Partner

logger = logging.getLogger(__name__)


class ValidatePartnerCloseout(APIView):

    def post(self, request):
        data = request.data
        validate = self.validate_units(data)
        if validate:
            return Response(
                "El socio tiene unidades activas. Primero debes venderlas antes de realizar la liquidación",
                status=status.HTTP_202_ACCEPTED
            )
        else:
            return Response(
                "Validación exitosa. El socio puede hacer el retiro.",
                status=status.HTTP_200_OK
            )

    def validate_units(self, data):
        partner = get_object_or_404(Partner, pk=data['partner'])
        units = partner.related_units.all()
        logger.exception("Unidades del socio {}: {} ".format(partner, units))
        logger.exception(units)
        if len(units) > 0:
            return True
        return False
