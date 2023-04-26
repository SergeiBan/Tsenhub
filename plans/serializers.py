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


class PlanSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Plan
        fields = ('pk', 'discount', 'name')
