from django.urls import path

from .api.views.charge_list import ChargeList
from .api.views.employee_create import EmployeeCreate
from .api.views.employee_delete import EmployeeDelete
from .api.views.employee_update import EmployeeUpdate
from .api.views.partner_list import PartnerList
from .api.views.validate_partner_withdraw import ValidatePartnerWithdraw
from .api.views.validate_partner_closeout import ValidatePartnerCloseout
from .api.views.partner_closeout import PartnerCloseout


app_name = "users"
urlpatterns = [
    path("<int:pk>/employee-detail", EmployeeUpdate.as_view(), name='employee_detail'),
    path("charge-list", ChargeList.as_view(), name='charge-list'),
    path("<int:pk>/employee-delete", EmployeeDelete.as_view(), name='employee_delete'),
    path("employee-create", EmployeeCreate.as_view(), name='employee_create'),
    path("<int:pk>/partner-list", PartnerList.as_view(), name='partner_list'),
    path("validate-withdraw", ValidatePartnerWithdraw.as_view(), name='validate_withdraw'),
    path("validate-closeout", ValidatePartnerCloseout.as_view(), name='validate_closeout'),
    path("closeout", PartnerCloseout.as_view(), name='closeout'),
]
