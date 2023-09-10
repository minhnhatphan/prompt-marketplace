"""
Serializer for the user API view
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the user model
    """
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'name']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5
            }
        }

    def create(self, validated_data):
        """
        Create and return a new user instance with encrypted password
        """
        return get_user_model().objects.create_user(**validated_data)
