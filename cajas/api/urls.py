from django.urls import include, path

app_name = 'api'
urlpatterns = [
    path('boxes/', include('cajas.boxes.urls', namespace='boxes'), name='boxes'),
    path('chains/', include('cajas.chains.urls', namespace='chains'), name='chains'),
    path('concepts/', include('cajas.concepts.urls', namespace='concepts'), name='concepts'),
    path('inventory/', include('cajas.inventory.urls', namespace='inventory'), name='inventory'),
    path('investments/', include('cajas.investments.urls', namespace='investments'), name='investments'),
    path('loans/', include('cajas.loans.urls', namespace='loans'), name='loans'),
    path('movements/', include('cajas.movement.urls', namespace='movements'), name='movements'),
    path('office/', include('cajas.office.urls', namespace='office'), name='office'),
    path('reports/', include('cajas.reports.urls', namespace='reports'), name='reports'),
    path('units/', include('cajas.units.urls', namespace='units'), name='units'),
    path('users/', include('cajas.users.urls', namespace='users'), name='users'),
]
