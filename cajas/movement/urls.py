from django.urls import path

from .api.views.movement_daily_square.accept_movement import AcceptMovement
from .api.views.movement_daily_square.create_movement import CreateDailySquareMovement
from .api.views.movement_daily_square.create_withdraw_movement import CreateWithdrawMovement
from .api.views.movement_daily_square.denied_movement import DeniedMovement
from .api.views.movement_daily_square.dispersion_movement import DispersionMovement
from .api.views.movement_don_juan_usd.movement_create import MovementUSDCreate
from .api.views.movement_office.movement_detail import MovementOfficeDetail
from .api.views.movement_office.movement_office_create import MovementOfficeCreate
from .api.views.movement_partner.movement_partner_create import MovementPartnerCreate
from .api.views.movement_request.movement_request_create import MovementRequestCreate
from .api.views.movement_request.movement_withdraw_request_create import MovementWithdrawRequestCreate
from .api.views.movement_request.accept_movement import AcceptRequestMovement
from .api.views.movement_request.accept_withdraw import AcceptWithDrawRequestMovement
from .api.views.movement_request.decline_movement import DeclineRequestMovement
from .api.views.movement_request.denied_withdraw import DeclineWithdrawMovement

app_name = 'movements'
urlpatterns = [
    path("create-mv-office/", MovementOfficeCreate.as_view(), name='movement-create'),
    path("create-dq-movement/", CreateDailySquareMovement.as_view(), name='create_dq_movement'),
    path("detail-mv-office/<int:pk>/", MovementOfficeDetail.as_view(), name='movement-office-detail'),
    path("accept-daily-square-movement/", AcceptMovement.as_view(), name='accept_daily_square_movement'),
    path("denied-daily-square-movement/", DeniedMovement.as_view(), name='denied_daily_square_movement'),
    path("dispersion-movement/", DispersionMovement.as_view(), name='dispersion_movement'),
    path("movement-partner-create/", MovementPartnerCreate.as_view(), name='movement_partner_create'),
    path("movement-request-create/", MovementRequestCreate.as_view(), name='movement_request_create'),
    path("movement-withdraw-request-create/", MovementWithdrawRequestCreate.as_view(),
         name='movement_withdraw_request_create'
         ),
    path("accept-request/", AcceptRequestMovement.as_view(), name='accept_request'),
    path("denied-request/", DeclineRequestMovement.as_view(), name='denied_request'),
    path("accept-withdraw-request/", AcceptWithDrawRequestMovement.as_view(), name='accept_withdraw_request'),
    path("denied-withdraw-request/", DeclineWithdrawMovement.as_view(), name='denied_withdraw_request'),
    path("create-withdraw-movement/", CreateWithdrawMovement.as_view(), name='withdraw_movement_create'),
    path("movement-usd-create/", MovementUSDCreate.as_view(), name='movement_usd_create'),
]
