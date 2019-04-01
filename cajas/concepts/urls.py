
from django.urls import path

from .api.views.concept_detail import ConceptDetail

app_name = 'concepts'
urlpatterns = [
    path("<int:pk>/", ConceptDetail.as_view(), name='concept_detail'),
]
