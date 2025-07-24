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
    model = User
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "name",
                    "phone_number",
                    "role",
                    "company",
                    "jshshir",
                    "image",
                )
            },
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
                    "company",
                    "image",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    list_display = [
        "username",
        "name",
        "role",
        "jshshir",
        "company",
        "is_superuser",
    ]
    list_filter = ("role", "company", "is_superuser")
    search_fields = ["name", "role", "jshshir"]
