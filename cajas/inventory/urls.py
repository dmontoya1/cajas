
from django.urls import path

from .api.views.brand_list import BrandList
from inventory.api.views.brand_list import BrandList

app_name = 'inventory'
urlpatterns = [
    path("<int:pk>/brand", BrandList.as_view(), name='brand_list'),
]
