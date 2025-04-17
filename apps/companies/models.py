from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.get_upload_path import get_upload_path


class Company(models.Model):
    """
    Model to represent different companies using the PPR system.
    Each company has their own equipment, users, and maintenance schedules.
    """

    name = models.CharField(_("Korxona nomi"), max_length=255)
    code = models.CharField(
        _("Korxona maxsus kodi"), max_length=50, unique=True
    )
    address = models.TextField(_("Manzil"), blank=True)
    contact_email = models.EmailField(_("Aloqa elektron pochtasi"), blank=True)
    contact_phone = models.CharField(
        _("Aloqa telefoni"), max_length=15, blank=True
    )
    logo = models.ImageField(
        _("Korxona logosi"), upload_to=get_upload_path, null=True, blank=True
    )
    is_active = models.BooleanField(_("Faol"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Korxona")
        verbose_name_plural = _("Korxonalar")

    def __str__(self):
        return self.name
