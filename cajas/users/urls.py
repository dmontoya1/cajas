from django.urls import path

from .api.views.employee_update import EmployeeUpdate

app_name = "users"
urlpatterns = [
    path("<int:pk>/employee-detail", EmployeeUpdate.as_view(), name='office-item-detail'),
]
