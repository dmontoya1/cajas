

from django.urls import path

from office.api.create_office_item import CreateOfficeItem
from office.api.office_item_delete import OfficeItemDelete
from office.api.office_item_detail import OfficeItemDetail


app_name = 'office'
urlpatterns = [
    path("<int:pk>/office-item-delete", OfficeItemDelete.as_view(), name='office_item'),
    path("<int:pk>/office-item-detail", OfficeItemDetail.as_view(), name='office_item_detail'),
    path("office-item-create", CreateOfficeItem.as_view(), name='office_item_create'),
]
