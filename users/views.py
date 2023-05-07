from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import response, status, viewsets
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import (CustomTokenObtainPairSerializer,
                               CustomUserRegisterSerializer, UserSerializer)

from .permissions import AnonCreateAuthReadUpdate
from users.tasks import notify_supplier


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    Все операции с пользователями.
    При создании пользователя в его поле сохраняется код
    будущего подтверждения регистрации.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AnonCreateAuthReadUpdate]

    def create(self, request, *args, **kwargs):
        serializer = CustomUserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = token_urlsafe(16)
        new_user = User.objects.create_user(
            **serializer.data,
            confirmation_token=token)
        new_user.send_register_confirmation(
            new_user.email, new_user.confirmation_token)
        return response.Response(
            self.get_serializer(new_user).data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path='verify-user')
    def verify_user(self, request):
        token = request.data.get('token')
        if not token:
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        user = get_object_or_404(User, confirmation_token=token)
        user.is_active = True
        user.confirmation_token = None
        user.save()
        refresh = RefreshToken.for_user(user)
        
        notify_supplier.delay(user.entity, user.email)
        return response.Response({
            'refresh': str(refresh), 'access': str(refresh.access_token),
            'role': user.role}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
