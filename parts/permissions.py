from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOnPlanPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.plan is not None
