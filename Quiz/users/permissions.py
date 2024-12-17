from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only teachers can access certain views
        return request.user.role == 'teacher'
