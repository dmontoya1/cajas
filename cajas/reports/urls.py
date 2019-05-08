
from django.urls import path


from .api.views.report_actives import ReportActive


app_name = 'reports'
urlpatterns = [
    path("report-actives", ReportActive.as_view(), name='report_active'),
]
