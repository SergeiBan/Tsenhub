from rest_framework import viewsets
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, PlanSerializer
from users.models import Plan


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer