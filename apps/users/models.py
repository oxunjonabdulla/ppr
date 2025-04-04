from audioop import reverse
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.get_upload_path import get_upload_path


class UserRole(models.TextChoices):
    """
        Default custom user roles for Backend.
    """

    SUPERUSER = "Superuser", _("Superuser")
    EquipmentMaster = "EquipmentMaster", _("Uskunalar ustasi")


class User(AbstractUser):
    """
    Default custom user model for Backend.
    """

    role = models.CharField(max_length="30", choices=UserRole.choices)
    name = models.CharField(_("User ismi"), blank=True, max_length=255)
    image = models.ImageField(verbose_name=_("User rasmi"),
                              upload_to=get_upload_path, null=True, blank=True)

    def get_absolute_url(self):
        """Get URL for user's detail view.
        Returns:
            str: URL for user detail.
        """
        return reverse("users:detail",
                       kwargs={"username": self.username})

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username} {self.name}"

    @property
    def get_full_name(self):
        return f"{self.name} {self.last_name}"

    def clean(self) -> None:
        if self.is_superuser:
            self.role = UserRole.SUPERUSER
        else:
            if self.role == UserRole.SUPERUSER:
                raise ValidationError(
                    message="If user is not superuser, role cannot be superuser",
                    code="Invalid parameter")
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