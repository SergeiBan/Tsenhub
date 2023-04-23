from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from users.models import Plan
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()


class UsernameField(serializers.Field):

    def to_representation(self, value):
        return super().to_representation(value)

    def to_internal_value(self, data):
        return f'{data} {timezone.now()}'


class CustomUserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'entity', 'password', )


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('pk', 'discount', 'name')


class UserSerializer(serializers.ModelSerializer):

    plan = PlanSerializer()

    class Meta:
        model = User
        fields = ('pk', 'email', 'entity', 'plan')


class UsersPlanSerializer(serializers.Serializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all()
    )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        data['role'] = self.user.role
        return data
