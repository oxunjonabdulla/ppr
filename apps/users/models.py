import re
from io import BytesIO

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image

from apps.utils.get_upload_path import get_upload_path


class UserRole(models.TextChoices):
    """
    User roles for PPR system.
    - SUPERUSER: Has full control over the entire system
    - COMPANY_ADMIN: Can manage their company's equipment masters, equipment and maintenance schedules
    - EQUIPMENT_MASTER: Can register equipment faults and maintenance activities
    - EQUIPMENT_OPERATOR: Basic user who uses equipment and receives notifications
    """

    SUPERUSER = "Superuser", _("Superuser")
    COMPANY_ADMIN = "CompanyAdmin", _(
        "Korxona Administratori"
    )  # Can manage their company
    EQUIPMENT_MASTER = "EquipmentMaster", _("Uskunalar ustasi")
    EQUIPMENT_OPERATOR = "EquipmentOperator", _("Uskunalar operatori")


class User(AbstractUser):
    """
    Default custom user model for Backend.
    """

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    role = models.CharField(max_length=30, choices=UserRole.choices)
    name = models.CharField(_("User ismi"), blank=True, max_length=255)
    phone_number = models.CharField(
        _("Telefon raqam"), max_length=15, blank=True
    )
    jshshir = models.CharField(
        _("JSHSHIR"),
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^\d{14}$",
                message=_(
                    "JSHSHIR aniq 14 ta raqamdan iborat bo'lishi kerak!"
                ),
            )
        ],
    )
    image = models.ImageField(
        verbose_name=_("User rasmi"),
        upload_to=get_upload_path,
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail", kwargs={"username": self.username})

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} {self.name}"

    @property
    def get_full_name(self):
        return f"{self.name} {self.last_name}"

    def clean(self) -> None:
        if not self.is_superuser:
            if not self.jshshir or not re.fullmatch(r"\d{14}", self.jshshir):
                raise ValidationError(
                    {
                        "jshshir": "JSHSHIR aniq 14 ta raqamdan iborat bo'lishi kerak!"
                    }
                )
            # Company admins and regular users must be associated with a company
            if (
                self.role
                in [
                    UserRole.COMPANY_ADMIN,
                    UserRole.EQUIPMENT_MASTER,
                    UserRole.EQUIPMENT_OPERATOR,
                ]
                and not self.company
            ):
                raise ValidationError(
                    {
                        "company": "Superuser bo'lmaganlar korxona bilan bog'langan bo'lishi kerak."
                    }
                )
        if self.is_superuser:
            self.role = UserRole.SUPERUSER
        else:
            if self.role == UserRole.SUPERUSER:
                raise ValidationError(
                    _(
                        "Agar user 'Superuser' bo'lmasa, role 'Superuser' bo'la olmaydi."
                    ),
                    code="invalid",
                )

        return super().clean()

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, "file"):
            img = Image.open(self.image)
            img = img.resize((300, 200), Image.Resampling.LANCZOS)
            img_io = BytesIO()
            img.save(img_io, format="PNG", quality=100)
            # Change the name of the saved image file to include the username
            filename = f"{self.username}_profile.png"
            self.image.save(filename, content=File(img_io), save=False)

        self.clean()
        super().save(*args, **kwargs)
