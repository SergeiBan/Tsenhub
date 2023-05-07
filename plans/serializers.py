from django.contrib.auth import get_user_model
from rest_framework import serializers

from plans.models import Plan

User = get_user_model()


class UsersPlanSerializer(serializers.Serializer):
    users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True
    )
    plan = serializers.PrimaryKeyRelatedField(
        queryset=Plan.objects.all()
    )


class FloatMultiplier(serializers.Field):
    def to_representation(self, value):
        return float(value)
    
    def to_internal_value(self, data):
        return data


class PlanSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)
    multiplier = FloatMultiplier()

    class Meta:
        model = Plan
        fields = ('pk', 'multiplier', 'name')


class RemovePlansSerializer(serializers.Serializer):

    plans = serializers.ListField(child=serializers.IntegerField(min_value=0))
