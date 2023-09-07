from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserMessages


class UserMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMessages
        fields = ['id', 'token', 'text']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'first_name']




