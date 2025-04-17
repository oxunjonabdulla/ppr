from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["username"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {"fields": ("name", "email", "role", "jshshir", "image")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # define the fields for the add user form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "jshshir",
                    "image",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = ["username", "name", "role", "jshshir", "is_superuser"]
    search_fields = ["name", "role", "jshshir"]
