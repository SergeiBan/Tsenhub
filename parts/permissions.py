from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsOnPlanPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        has_plan_assigned = hasattr(User, 'plan')
        return request.user.is_authenticated and has_plan_assigned
