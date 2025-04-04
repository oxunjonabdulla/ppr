from rest_framework import permissions

from apps.users.models import UserRole


class BaseRolePermission(permissions.BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        return request.user.is_authinticated and request.user.role in self.allowed_roles


class IsEquipmentMaster(BaseRolePermission):
    allowed_roles = [UserRole.SUPERUSER, UserRole.EquipmentMaster]
