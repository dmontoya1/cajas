from django.urls import path

from .views.arc_request import ArcRequest
from .views.box_don_juan_office import BoxDonJuanOffice
from .views.chain_create import ChainCreate
from .views.chain_list import ChainList
from .views.chain_payments import ChainPayments
from .views.chain_places_list import ChainPlacesList
from .views.create_daily_square_movement import CreateDailySquareMovement
from .views.create_don_juan_movement import CreateDonJuanMovement
from .views.create_office_movement import CreateOfficeMovement
from .views.daily_square_box import DailySquareBox
from .views.daily_square_list import DailySquareList
from .views.employee_list import EmployeeList
from .views.home_view import Home
from .views.loan_create import LoanCreate
from .views.loan_list import LoanList
from .views.loan_payment_list import LoanPaymentList
from .views.movement_requirement_list import MovementRequireList
from .views.movement_withdraw_requirement_list import MovementWithdrawRequireList
from .views.office_box import OfficeBox
from .views.office_items_list import OfficeItemsList
from .views.partner_box import PartnerBox
from .views.partner_create import PartnerCreate
from .views.partner_list import PartnerList
from .views.partner_unit import PartnerUnitsList
from .views.units_list import UnitsList


app_name = 'webclient'

urlpatterns = [
    path("", Home.as_view(), name='home'),
    path("arqueo/", ArcRequest.as_view(), name='arc_request'),
    path("movement-require/", MovementRequireList.as_view(), name='movement_required'),
    path("movement-withdraw-require/", MovementWithdrawRequireList.as_view(), name='movement_withdraw_required'),

    # Office
    path("office/<slug:slug>/", OfficeBox.as_view(), name='office'),
    path("office/<slug:slug>/items/", OfficeItemsList.as_view(), name='office_items_list'),
    path("office/<slug:slug>/create-office-movement/", CreateOfficeMovement.as_view(), name='create_office_movement'),

    # DonJuan
    path("office/<slug:slug>/donjuan/", BoxDonJuanOffice.as_view(), name='box_don_juan'),
    path("office/<slug:slug>/create-donjuan-movement/", CreateDonJuanMovement.as_view(),
         name='create_donjuan_movement'),

    # Partners
    path("office/<slug:slug>/partner/<int:pk>/box/", PartnerBox.as_view(), name='partner_box'),
    path("office/<slug:slug>/partners/", PartnerList.as_view(), name='partners_list'),
    path("partner/add/", PartnerCreate.as_view(), name='partner_add'),

    # Employees
    path("employee/<slug:slug>/employee-list/", EmployeeList.as_view(), name='employee-list'),

    # Daily Square
    path("office/<slug:slug>/daily-square/", DailySquareList.as_view(), name='daily_square_list'),
    path("office/<slug:slug>/daily-square/<int:pk>/box/", DailySquareBox.as_view(), name='daily_square_box'),
    path("create-daily-square-movement/", CreateDailySquareMovement.as_view(), name='add_daily_square_movement'),

    # Loans
    path("office/<slug:slug>/loan-list/", LoanList.as_view(), name='loan_list'),
    path("office/<slug:slug>/loan/<int:pk>/payments/", LoanPaymentList.as_view(), name='loan_payment_list'),
    path("office/<slug:slug>/loan-create/", LoanCreate.as_view(), name='loan_create'),

    # Chains
    path("office/<slug:slug>/chain-list/", ChainList.as_view(), name='chain_list'),
    path("office/<slug:slug>/chain-list/<int:pk>/", ChainPlacesList.as_view(), name='chain_places_list'),
    path("office/<slug:slug>/chain-create/", ChainCreate.as_view(), name='chain_create'),

    path("create-daily-square-movement/", CreateDailySquareMovement.as_view(), name='add_daily_square_movement'),
    path("units/<slug:slug>/units-list/", UnitsList.as_view(), name='units_list'),
    path("units/<slug:slug>/<int:pk>/units-list/", PartnerUnitsList.as_view(), name='partner_units_list'),

    path("office/<slug:slug>/chain-payments/<int:pk>/", ChainPayments.as_view(), name='chain_payments'),

]
