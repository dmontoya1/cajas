from django.urls import path

from .api.views.movement_office.movement_office_create import MovementOfficeCreate
from .api.views.movement_office.movement_detail import MovementOfficeDetail

app_name = 'movements'
urlpatterns = [
    path(
        "create-mv-office/",
        MovementOfficeCreate.as_view(),
        name='movement-create'
    ),
    path(
        "detail-mv-office/<int:pk>/",
        MovementOfficeDetail.as_view(),
        name='movement-office-detail'
    ),
]
