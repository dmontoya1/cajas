
from django.urls import path

from inventory.api.brand_list import BrandList

app_name = 'inventory'
urlpatterns = [
    path("<int:pk>/brand", BrandList.as_view(), name='brand_list'),
]
