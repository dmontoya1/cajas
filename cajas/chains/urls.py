from django.urls import path

from .api.views.chain_create import ChainCreate
from .api.views.user_place_pay_create import UserPlacePayCreate
from .api.views.update_user_place import UserPlaceUpdate

app_name = 'chains'
urlpatterns = [
    path(
        "create/",
        ChainCreate.as_view(),
        name='chain_create'
    ),
    path(
        "add-user-pay/",
        UserPlacePayCreate.as_view(),
        name='user_place_pay'
    ),
    path(
        "edit-place/",
        UserPlaceUpdate.as_view(),
        name='user_place_update'
    ),

]
