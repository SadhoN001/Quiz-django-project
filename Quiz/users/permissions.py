from rest_framework import permissions
from rest_framework.permissions import BasePermission

# class IsTeacher(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # Check if the 'role' is set and equals 'teacher'
#         return getattr(request.user, 'role', None) == 'teacher'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        is_teacher = hasattr(request.user, 'teacher_profile')
        if not is_teacher:
            print(f"Permission Denied: {request.user} is not a teacher.")
        return is_teacher

