
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class ReportActive(APIView):

    def get(self, request):
        return Response(
            "Test",
            status=status.HTTP_200_OK
        )
