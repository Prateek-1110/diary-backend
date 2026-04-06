from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Object-level permission: allow access only if obj.user == request.user.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user