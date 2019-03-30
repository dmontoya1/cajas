
from rest_framework import generics

from ...models.concepts import Concept
from ..serializers.concept_serializer import ConceptSerializer


class ConceptDetail(generics.RetrieveAPIView):

    serializer_class = ConceptSerializer
    queryset = Concept.objects.all()

