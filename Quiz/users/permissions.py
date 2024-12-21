from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the 'role' is set and equals 'teacher'
        return getattr(request.user, 'role', None) == 'teacher'


