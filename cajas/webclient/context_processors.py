
from django.conf import settings


def webclient_processor(request):

    context = {
        'API_KEY': settings.API_KEY,
    }
    
    return context
