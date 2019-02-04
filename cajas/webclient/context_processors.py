
from django.conf import settings

from concepts.models.concepts import Concept


def webclient_processor(request):

    concepts = Concept.objects.filter(is_active=True)

    context = {
        'API_KEY': settings.API_KEY,
        'concepts': concepts,
    }
    
    return context
