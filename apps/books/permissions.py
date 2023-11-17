from ninja_extra import permissions, api_controller, http_get


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.method in permissions.SAFE_METHODS


class LoginRequired(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method not in permissions.SAFE_METHODS:
            user = request.user or request.auth  # type: ignore
            return bool(user and user.is_authenticated)
        return True

