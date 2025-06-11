# --- File: users/serializers.py ---
# Serializers for Djoser to handle user data.
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Serializer for creating new users (registration)
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Serializer for user details (after registration/login)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username')

# --- File: users/urls.py ---
# User specific URLs (optional for MVP, Djoser handles most auth)
from django.urls import path

urlpatterns = [
    # Add any user-specific URLs here if needed beyond Djoser's defaults
]
