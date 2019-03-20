from django.urls import path

from .api.views.charge_list import ChargeList
from .api.views.employee_create import EmployeeCreate
from .api.views.employee_delete import EmployeeDelete
from .api.views.employee_update import EmployeeUpdate

app_name = "users"
urlpatterns = [
    path("<int:pk>/employee-detail", EmployeeUpdate.as_view(), name='employee_detail'),
    path("charge-list", ChargeList.as_view(), name='charge-list'),
    path("<int:pk>/employee-delete", EmployeeDelete.as_view(), name='employee_delete'),
    path("employee-create", EmployeeCreate.as_view(), name='employee_create'),
]
