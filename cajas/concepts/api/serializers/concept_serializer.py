
from rest_framework import serializers

from ...models.concepts import Concept


class ConceptSerializer(serializers.ModelSerializer):

    concept_type = serializers.SerializerMethodField()
    relationship = serializers.SerializerMethodField()

    class Meta:
        model = Concept
        fields = ('id', 'name', 'description', 'concept_type', 'relationship', 'counterpart', 'is_active')


    def get_concept_type(self, obj):
        return str(obj.concept_type)

    def get_relationship(self, obj):
        return str(obj.relationship)
