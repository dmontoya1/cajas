
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
        date = request.query_params.get('date', None)
        date = datetime.strptime(date, '%Y-%m-%d')
        RankingOffice.objects.filter(
            month__month=date.month,
            month__year=date.year
        ).delete()
        RankingOffice.objects.create(
            fields=data,
            month=date
        )

        return Response(
            "Se ha guardado con exito",
            status=status.HTTP_200_OK
        )
