
from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from cajas.api.CsrfExempt import CsrfExemptSessionAuthentication

from ...models import RankingOffice


class ReportRankingSave(APIView):

    authentication_classes = (CsrfExemptSessionAuthentication,)

    def post(self, request):
        data = request.data
        start_date = request.query_params.get('start_date', None)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = request.query_params.get('end_date', None)
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        RankingOffice.objects.filter(
            start_date=start_date,
            end_date=end_date
        ).delete()
        RankingOffice.objects.create(
            fields=data,
            start_date=start_date,
            end_date=end_date
        )

        return Response(
            "Se ha guardado con exito",
            status=status.HTTP_200_OK
        )
