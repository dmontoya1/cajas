

from django.urls import path

from cajas.office.api.create_office_item import CreateOfficeItem
from .api.create_supervisor_calendar import CreateSupervisorCalendar
from .api.create_group import CreateGroup
from .api.group_detail import GroupDetail
from cajas.office.api.office_item_delete import OfficeItemDelete
from cajas.office.api.office_item_detail import OfficeItemDetail
from .api.supervisor_calendar_list import SupervisorCalendarList
from .api.supervisor_calendar_delete import SupervisorCalendarDelete

app_name = 'office'
urlpatterns = [
    path("<int:pk>/office-item-delete", OfficeItemDelete.as_view(), name='office_item_delete'),
    path("<int:pk>/office-item-detail", OfficeItemDetail.as_view(), name='office_item_detail'),
    path("office-item-create", CreateOfficeItem.as_view(), name='office_item_create'),
    path("group-create", CreateGroup.as_view(), name='group_create'),
    path("<int:pk>/group-detail", GroupDetail.as_view(), name='group_detail'),
    path("<int:pk>/supervisor-calendar-delete", SupervisorCalendarDelete.as_view(), name='office_item_delete'),
    path("supervisor-calendar-create", CreateSupervisorCalendar.as_view(), name='supervisor_calendar_create'),
    path("supervisor-calendar-list", SupervisorCalendarList.as_view(), name='supervisor_calendar_list'),
]
