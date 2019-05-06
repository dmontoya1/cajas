
from django.conf import settings

from cajas.users.models.partner import Partner
from cajas.concepts.models.concepts import Concept


def webclient_processor(request):
    if 'office' in request.session:
        partners = Partner.objects.filter(office__pk=request.session['office'], is_active=True)
    else:
        partners = None
    all_partners = Partner.objects.filter(is_active=True)
    concepts = Concept.objects.filter(is_active=True)
    context = {
        'API_KEY': settings.API_KEY,
        'concepts': concepts,
        'partners': partners,
        'all_partners': all_partners,
    }

    return context
