

from django.urls import path

from office.api.office_item_delete import OfficeItemDelete
from office.api.office_item_detail import OfficeItemDetail


app_name = 'office'
urlpatterns = [
    path("<int:pk>/office-item-delete", OfficeItemDelete.as_view(), name='office-item'),
    path("<int:pk>/office-item-detail", OfficeItemDetail.as_view(), name='office-item-detail'),
]
