from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allow access to admin users, read-only for others
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  
            return True # Allow read-only access for all users
        return request.user and request.user.is_staff # Allow admin access only