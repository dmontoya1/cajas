from django.urls import include, path

app_name = 'api'
urlpatterns = [
    path('movements/', include('movement.urls', namespace='movements'), name='movements'),
    path('units/', include('units.urls', namespace='units'), name='units'),
]
