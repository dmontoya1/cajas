
from datetime import datetime

from django.http import JsonResponse

from rest_framework.views import APIView


from ...models import RankingOffice


class ReportRankingLoad(APIView):

    def get(self, request):
        date = request.query_params.get('date', None)
        date = datetime.strptime(date, '%Y-%m-%d')
        print(RankingOffice.objects.all())
        ranking = RankingOffice.objects.filter(
            month__month=date.month,
            month__year=date.year
        )
        print(ranking)
        data = list(ranking.values())
        return JsonResponse(
            data,
            safe=False
        )
