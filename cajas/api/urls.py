from django.urls import include, path
from django.contrib import admin
from . import views

app_name = 'api'
urlpatterns = [
    path('movements/', include('movement.urls', namespace='movements'), name='movements'),
    # url(r'^devices/$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    # url(r'^api-key/', views.ApiKeyDetailView.as_view(), name='api-key' ),
    # url(r'^manager/', include('manager.urls', namespace="api-manager")),
    # url(r'^routes/', include('routes.urls')),
    # url(r'^schools/', include('schools.urls')),
    # url(r'^users/', include('users.urls')),
    # url(r'^auth/', include('rest_auth.urls')),
    # url(r'^auth/registration/', include('rest_auth.registration.urls')),
    # url(r'^docs/', include('rest_framework_docs.urls')),
]
