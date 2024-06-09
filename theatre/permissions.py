from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        is_safe_method = request.method in SAFE_METHODS
        is_authenticated = request.user and request.user.is_authenticated
        is_admin = request.user and request.user.is_staff

        return bool((is_safe_method and is_authenticated) or is_admin)
