from rest_framework.permissions import BasePermission
from django.utils import timezone


class HasValidAccess(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        access_end = user.created_at + user.access_duration

        if timezone.now() > access_end:
            return False

        return True
    



class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user    