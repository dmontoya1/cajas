from django.urls import path

from .api.views.chain_create import ChainCreate

app_name = 'chains'
urlpatterns = [
    path(
        "create/",
        ChainCreate.as_view(),
        name='chain_create'
    ),

]
