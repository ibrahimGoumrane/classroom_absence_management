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
    Allows access only to teacher users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == 'teacher')        
    
class TeacherOwnObjects(BasePermission):
    """
    Allows teachers to access only their own objects.
    """
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.role == 'teacher' and 
                   hasattr(obj, 'teacher') and obj.teacher == request.user.teacher_profile)  


class IsTeacherOrAdmin(BasePermission):
    """
    Allows access to admin users or teachers.
    """
    def has_permission(self, request, view):
        return bool((request.user and request.user.role == 'teacher') or 
                    (request.user and request.user.role == 'admin'))

class TeacherObjectOwnerOrAdmin(BasePermission):
    """
    Allows access to object owners (teachers) or admins.
    """
    def has_object_permission(self, request, view, obj):
        # Admin check
        is_admin = bool(request.user and request.user.role == 'admin')
        
        # Teacher ownership check
        is_teacher_owner = bool(request.user and 
                               request.user.role == 'teacher' and
                               hasattr(obj, 'teacher') and 
                               obj.teacher == request.user.teacher_profile)
                               
        return is_admin or is_teacher_owner