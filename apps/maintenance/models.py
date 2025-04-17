from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.utils.get_upload_path import get_upload_path

#  Ta'mirlash jadvali
# ------------------------------------------------------------------------------------------


class MaintenanceSchedule(models.Model):
    """
    Model for scheduling equipment maintenance.
    """

    MAINTENANCE_TYPE_CHOICES = (
        ("preventive", _("Oldini olish")),
        ("corrective", _("Tuzatish")),
        ("condition_based", _("Holatga asoslangan")),
        ("predictive", _("Bashoratli")),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    maintenance_type = models.CharField(
        _("Xizmat turi"),
        max_length=25,
        choices=MAINTENANCE_TYPE_CHOICES,
        default="preventive",
    )
    title = models.CharField(_("Nomi"), max_length=255, blank=True)
    description = models.TextField(_("Ta'rif"), blank=True)
    scheduled_date = models.DateTimeField(
        _("Rejalashtirilgan sana"), null=True, blank=True
    )
    estimated_duration = models.PositiveIntegerField(
        _("Taxminiy muddat"), default=1, null=True, blank=True
    )
    assigned_to = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="assigned_maintenance",
        null=True,
        blank=True,
    )
    is_completed = models.BooleanField(_("Bajarildi"), default=False)
    completed_date = models.DateTimeField(
        _("Bajarilgan vaqti"), null=True, blank=True
    )
    completed_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="completed_maintenance",
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="created_schedules",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content_object} uchun {self.scheduled_date} kuni texnik xizmat ko'rsatish"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # I can handle updates to content_object if it has next_maintenance or last_maintenance
        obj = self.content_object
        fields_to_update = []

        if hasattr(obj, "next_maintenance") and not self.is_completed:
            if (
                not obj.next_maintenance
                or self.scheduled_date < obj.next_maintenance
            ):
                obj.next_maintenance = self.scheduled_date
                fields_to_update.append("next_maintenance")

        if (
            hasattr(obj, "last_maintenance")
            and self.is_completed
            and self.completed_date
        ):
            if (
                not obj.last_maintenance
                or self.completed_date > obj.last_maintenance
            ):
                obj.last_maintenance = self.completed_date
                fields_to_update.append("last_maintenance")

        if fields_to_update:
            obj.save(update_fields=fields_to_update)


# Xizmat haqida ogohlantirish
# ------------------------------------------------------------------------------------------


class MaintenanceWarning(models.Model):
    """
    Model for maintenance warnings sent to user
    """

    WARNING_LEVELS = (
        ("low", _("Past")),
        ("medium", _("O‘rta")),
        ("high", _("Yuqori")),
        ("critical", _("Favqulodda")),
    )
    maintenance_schedule = models.ForeignKey(
        MaintenanceSchedule, on_delete=models.CASCADE, related_name="warnings"
    )
    warning_level = models.CharField(
        _("Ogohlantirish darajasi"),
        max_length=15,
        choices=WARNING_LEVELS,
        default="medium",
    )
    days_before = models.PositiveIntegerField(
        _("Belgilangan sanadan bir necha kun oldin"),
        default=10,
        null=True,
        blank=True,
    )
    message = models.TextField(_("Ogohlantirish xabari"), blank=True)
    is_sent = models.BooleanField(_("Yuborildi"), default=False)
    sent_date = models.DateTimeField(
        _("Yuborilgan sana"), null=True, blank=True
    )

    class Meta:
        verbose_name = _("Maintenance Warning")
        verbose_name_plural = _("Maintenance Warnings")

    def __str__(self):
        return f"{self.get_warning_level_display()}  {self.maintenance_schedule.title} uchun ogohlantirish"


# Uskuna nosozligi
# ------------------------------------------------------------------------------------------
class EquipmentFault(models.Model):
    """
    Model for recording equipment faults by equipment masters.
    Includes timestamp and photo evidence.
    """

    FAULT_SEVERITY = (
        ("minor", _("Yengil")),
        ("moderate", _("O‘rtacha")),
        ("major", _("Jiddiy")),
        ("critical", _("Favqulodda")),
    )

    # Generic Foreign Key setup
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    equipment = GenericForeignKey("content_type", "object_id")

    title = models.CharField(_("Nosozlik nomi"), max_length=255, blank=True)
    description = models.TextField(_("Ta'rifi"), blank=True)
    severity = models.CharField(
        _("Holati"), max_length=10, choices=FAULT_SEVERITY, default="moderate"
    )
    photo = models.ImageField(
        _("Rasmi"),
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])
        ],
    )
    capture_time = models.DateTimeField(
        _("Suratga olish vaqti"), null=True, blank=True
    )
    reported_at = models.DateTimeField(
        _("Xabar berilgan vaqti"), auto_now_add=True
    )
    reported_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="reported_faults",
        null=True,
    )
    is_resolved = models.BooleanField(_("Yechilgan"), default=False)
    resolved_at = models.DateTimeField(
        _("Hal qilingan vaqt"), null=True, blank=True
    )
    resolved_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="resolved_faults",
        null=True,
        blank=True,
    )
    resolution_notes = models.TextField(_("Nosozlik haqida izoh"), blank=True)
    gps_location = models.CharField(
        _("GPS location"), max_length=255, blank=True, null=True
    )

    class Meta:
        verbose_name = _("Uskunalar nosozligi")
        verbose_name_plural = _("Uskunalar nosozliklari")

    def __str__(self):
        return f"{self.title} - {self.equipment}"


# Bildirishnoma jurnali
# ------------------------------------------------------------------------------------------


class Notification(models.Model):
    """
    Model for system notifications to users and Telegram group
    """

    NOTIFICATION_TYPE = (
        (
            "maintenance_due",
            _("Texnik xizmat muddati yaqinlashmoqda"),
        ),  # Maintenance Due
        (
            "maintenance_completed",
            _("Texnik xizmat bajarildi"),
        ),  # Maintenance Completed
        ("fault_reported", _("Nosozlik aniqlandi")),  # Fault Reported
        ("fault_resolved", _("Nosozlik bartaraf etildi")),  # Fault Resolved
        ("system", _("Tizim xabarnomasi")),  # System Notification
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="notifications",
        null=True,
        blank=True,
    )
    title = models.CharField(
        _("Xabarnoma sarlavhasi"), max_length=255, blank=True
    )
    message = models.TextField(_("Xabarnoma matni"), blank=True)
    notification_type = models.CharField(
        _("Xabarnoma turi"),
        max_length=25,
        choices=NOTIFICATION_TYPE,
        default="maintenance_due",
    )
    created_at = models.DateTimeField(_("Yaratilgan vaqti"), auto_now_add=True)
    is_read = models.BooleanField(_("O‘qilgan"), default=False)
    read_at = models.DateTimeField(_("O‘qilgan vaqti"), null=True, blank=True)
    sent_to_telegram = models.BooleanField(
        _("Telegramga yuborilgan"), default=False
    )

    class Meta:
        verbose_name = _("Xabarnoma")
        verbose_name_plural = _("Xabarnomalar")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"
