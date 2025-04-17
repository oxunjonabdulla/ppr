from rest_framework import permissions

from apps.users.models import UserRole


def is_same_company(user, obj):
    """
    Helper function to check if the object's company matches the user's company
    """
    if hasattr(obj, "company"):
        return obj.company == user.company
    elif hasattr(obj, "equipment") and hasattr(obj.equipment, "company"):
        return obj.equipment.company == user.company
    return False


class BaseCompanyPermission(permissions.BasePermission):
    """
    Base permissions class that allows superusers or same company users.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return is_same_company(request.user, obj)


class IsSuperUser(permissions.BasePermission):
    """Permissions for superusers only"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class IsCompanyAdmin(BaseCompanyPermission):
    """Permissions for company administrators"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser)
            or request.user.role == UserRole.COMPANY_ADMIN
        )


class IsEquipmentMaster(BaseCompanyPermission):
    """Permissions for equipment masters and company admins"""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser)
            or request.user.role
            in [UserRole.COMPANY_ADMIN, UserRole.EQUIPMENT_MASTER]
        )


class IsEquipmentOperator(BaseCompanyPermission):
    """Permissions for equipment operators"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.role == UserRole.EQUIPMENT_OPERATOR
        )


class CompanyUserPermission(BaseCompanyPermission):
    """
    Generic permission class for any authenticated compnay user
    to access their own company's objects.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated
