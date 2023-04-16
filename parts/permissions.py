from rest_framework import permissions
from django.contrib.auth import get_user_model


User = get_user_model()


class IsInGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        has_group_assigned = hasattr(User, 'group')
        return request.user.is_superuser or has_group_assigned