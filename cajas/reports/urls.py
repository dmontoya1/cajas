
from django.urls import path


from .api.views.report_actives import ReportActive
from .api.views.report_debt import ReportDebt
from .api.views.report_employee_salary import ReportEmployeeSalary
from .api.views.report_ranking_save import ReportRankingSave
from .api.views.report_ranking_load import ReportRankingLoad


app_name = 'reports'
urlpatterns = [
    path("report-actives", ReportActive.as_view(), name='report_active'),
    path("report-debt", ReportDebt.as_view(), name='report_debt'),
    path("report-employee-salary", ReportEmployeeSalary.as_view(), name='report_employee_salary'),
    path("report-ranking-save", ReportRankingSave.as_view(), name='report_ranking_save'),
    path("report-ranking-load", ReportRankingLoad.as_view(), name='report_ranking_load'),
]
