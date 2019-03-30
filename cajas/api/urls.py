from django.urls import include, path

app_name = 'api'
urlpatterns = [
    path('boxes/', include('boxes.urls', namespace='boxes'), name='boxes'),
    path('chains/', include('chains.urls', namespace='chains'), name='chains'),
    path('concepts/', include('concepts.urls', namespace='concepts'), name='concepts'),
    path('inventory/', include('inventory.urls', namespace='inventory'), name='inventory'),
    path('loans/', include('loans.urls', namespace='loans'), name='loans'),
    path('movements/', include('movement.urls', namespace='movements'), name='movements'),
    path('office/', include('office.urls', namespace='office'), name='office'),
    path('units/', include('units.urls', namespace='units'), name='units'),
    path('users/', include('users.urls', namespace='users'), name='users'),
]
