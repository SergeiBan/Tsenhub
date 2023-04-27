from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (TokenObtainPairSerializer,
                                                  TokenRefreshSerializer)
from rest_framework_simplejwt.views import TokenObtainPairView

from plans.serializers import PlanSerializer

User = get_user_model()


class UsernameField(serializers.Field):

    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, data):
        return f'{data} {timezone.now()}'


class CustomUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'entity', 'password')


class UserSerializer(serializers.ModelSerializer):

    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ('pk', 'email', 'entity', 'plan')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.context['request'].user.is_authenticated
        return data
