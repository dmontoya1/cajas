
from datetime import datetime

from django.http import JsonResponse

from rest_framework.views import APIView


from ...models import RankingOffice


class ReportRankingLoad(APIView):

    def get(self, request):
        start_date = request.query_params.get('start_date', None)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = request.query_params.get('end_date', None)
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        ranking = RankingOffice.objects.filter(
            start_date=start_date,
            end_date=end_date
        )
        data = list(ranking.values())
        return JsonResponse(
            data,
            safe=False
        )
