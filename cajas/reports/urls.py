
from django.urls import path


from .api.views.report_actives import ReportActive
from .api.views.report_debt import ReportDebt


app_name = 'reports'
urlpatterns = [
    path("report-actives", ReportActive.as_view(), name='report_active'),
    path("report-debt", ReportDebt.as_view(), name='report_debt'),
]
