# serializers.py

from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'created_at', 'updated_at', 'is_active', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}
