# accounts/permissions.py
from rest_framework.permissions import BasePermission

class IsAccessValid(BasePermission):
    """
    Allows access only if user's access duration is still valid.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_valid_access()
