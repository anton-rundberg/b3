from rest_framework.permissions import BasePermission


class PasswordPermission(BasePermission):
    message = "Invalid password"

    def has_permission(self, request, view):
        return request.user.check_password(request.data.get("password", None))
