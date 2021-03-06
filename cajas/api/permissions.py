from rest_framework import permissions
from .models import APIKey


class HasAPIAccess(permissions.BasePermission):
    """
    Clase para dar permisos de a las API
    """
    message = 'Invalid or missing API Key.'

    def has_permission(self, request, view):
        api_key = request.META.get('HTTP_API_KEY', '')
        return APIKey.objects.filter(key=api_key).exists()
