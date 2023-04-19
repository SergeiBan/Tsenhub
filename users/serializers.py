from rest_registration.api.serializers import DefaultRegisterUserSerializer
from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Plan


User = get_user_model()


class UsernameField(serializers.Field):

    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, data):
        return f'{data} {timezone.now()}'


class CustomUserRegisterSerializer(DefaultRegisterUserSerializer):

    username = UsernameField()


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('discount', 'name')


class UserSerializer(serializers.ModelSerializer):

    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ('email', 'username', 'plan')