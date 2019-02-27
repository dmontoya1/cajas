from django.urls import path

from .api.views.movement_office.movement_office_create import MovementOfficeCreate
from .api.views.movement_office.movement_detail import MovementOfficeDetail
from .api.views.movement_daily_square.accept_movement import AcceptMovement
from .api.views.movement_daily_square.denied_movement import DeniedMovement
from .api.views.movement_daily_square.dispersion_movement import DispersionMovement

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
    path(
        "accept-daily-square-movement/",
        AcceptMovement.as_view(),
        name='accept_daily_square_movement'
        ),
    path(
        "denied-daily-square-movement/",
        DeniedMovement.as_view(),
        name='denied_daily_square_movement'
    ),
    path(
        "dispersion-movement/",
        DispersionMovement.as_view(),
        name='dispersion-movement'
    ),
]
