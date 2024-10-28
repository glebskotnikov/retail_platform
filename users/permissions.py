from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Allows access only to active employees.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and (request.user.is_staff or request.user.is_superuser)
        )
