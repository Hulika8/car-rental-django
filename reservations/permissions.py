from rest_framework.permissions import BasePermission


class IsAdminOrOwner(BasePermission):
    """
    Admin can see all reservations.
    Normal users can only see their own reservations.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user