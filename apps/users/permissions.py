from rest_framework.permissions import BasePermission

class IsAdminOrOwner(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can do anything
        if request.user and request.user.role == 'admin':
            return True
        # Owners can edit or delete their own account
        return obj == request.user
    
class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'admin')    
    

class IsTeacher(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'teacher')        