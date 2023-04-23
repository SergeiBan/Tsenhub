from rest_framework.permissions import BasePermission


class AnonCreateAuthReadUpdate(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == 'POST' or
            (request.user.is_authenticated and
             request.user.role == 'supplier')):
            return True
        return False


class IsSupplier(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'supplier':
            return True
        return False
