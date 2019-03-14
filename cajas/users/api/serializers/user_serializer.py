from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    """

    #category = CateogrySerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = '__all__'