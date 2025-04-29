from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.get_upload_path import get_upload_path

#  Ta'mirlash jadvali
# ------------------------------------------------------------------------------------------


class MaintenanceSchedule(models.Model):
    MAINTENANCE_TYPE_CHOICES = (
        # General maintenance types (applicable to multiple equipment types)
        ("inspection", _("Texnik ko'rik")),
        ("full_inspection", _("To'liq texnik ko'rik")),
        ("partial_inspection", _("Qisman texnik ko'rik")),
        # Electrical/measurement checks
        ("voltmeter_check", _("Voltmetr tekshiruvi")),
        ("manometer_check", _("Manometr tekshiruvi")),
        # Mechanical/hydraulic tests
        ("hydraulic_test", _("Gidravlik sinov")),
        ("pressure_test", _("Bosim sinovi")),
        # Cleaning/flushing procedures
        ("flush_test", _("Yuvish va sinov")),
        ("inner_outer_check", _("Ichki/tashqi tekshiruv")),
        # Specialized tests
        ("lab_test", _("Laboratoriya tekshiruvi")),
        ("leveling_check", _("Nivelirovka tekshiruvi")),
        ("safety_valve_check", _("Xavfsizlik klapani tekshiruvi")),
        # Additional checks
        ("lubrication_check", _("Yog'lash tekshiruvi")),
        ("alignment_check", _("Markalash tekshiruvi")),
        ("calibration_check", _("Kalibrlash tekshiruvi")),
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    maintenance_type = models.CharField(
        _("Texnik xizmat turi"),
        max_length=50,
        choices=MAINTENANCE_TYPE_CHOICES,
    )
    description = models.TextField(_("Ta'rif"), blank=True)
    scheduled_date = models.DateField(
        _("Ko'rik sanasi"), null=True, blank=True
    )
    estimated_unit = models.CharField(
        _("Taxminiy muddat birligi"),
        max_length=10,
        choices=[("days", _("Kun")), ("months", _("Oy")), ("years", _("Yil"))],
        default="days",
    )
    estimated_value = models.PositiveIntegerField(
        _("Taxminiy muddat qiymati"), default=1
    )
    next_maintenance_date = models.DateField(
        _("Keyingi ko'rik sanasi"), null=True, blank=True
    )

    assigned_to = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="assigned_maintenance",
        null=True,
        blank=True,
    )

    is_completed = models.BooleanField(_("Bajarildi"), default=False)
    completed_date = models.DateField(
        _("Bajarilgan sana"), null=True, blank=True
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
        return f"{self.get_maintenance_type_display()} - {self.scheduled_date}"

    def save(self, *args, **kwargs):
        if (
            self.scheduled_date
            and self.estimated_value
            and self.estimated_unit
        ):
            if self.estimated_unit == "days":
                self.next_maintenance_date = self.scheduled_date + timedelta(
                    days=self.estimated_value
                )
            elif self.estimated_unit == "months":
                self.next_maintenance_date = (
                    self.scheduled_date
                    + relativedelta(months=self.estimated_value)
                )
            elif self.estimated_unit == "years":
                self.next_maintenance_date = (
                    self.scheduled_date
                    + relativedelta(years=self.estimated_value)
                )
        super().save(*args, **kwargs)


# Xizmat haqida ogohlantirish
# ------------------------------------------------------------------------------------------


class MaintenanceWarning(models.Model):
    WARNING_TIME = (
        ("one_month", _("1 oy oldin")),
        ("fifteen_days", _("15 kun oldin")),
        ("seven_days", _("7 kun oldin")),
        ("three_days", _("3 kun oldin")),
    )
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
    warning_time = models.CharField(
        _("Ogohlantirish vaqti"), max_length=20, choices=WARNING_TIME
    )
    message = models.TextField(_("Ogohlantirish xabari"), blank=True)
    is_sent = models.BooleanField(_("Yuborildi"), default=False)
    sent_date = models.DateTimeField(
        _("Yuborilgan sana"), null=True, blank=True
    )
    sent_to_telegram = models.BooleanField(
        _("Telegramga yuborilgan"), default=False
    )

    class Meta:
        verbose_name = _("Maintenance Warning")
        verbose_name_plural = _("Maintenance Warnings")
        unique_together = (
            "maintenance_schedule",
            "warning_level",
        )  # Prevent duplicate warnings

    def __str__(self):
        return (
            f"{self.get_warning_level_display()} - {self.maintenance_schedule}"
        )


# Uskuna nosozligi
# ------------------------------------------------------------------------------------------
class EquipmentFault(models.Model):
    FAULT_SEVERITY = (
        ("minor", _("Yengil")),
        ("moderate", _("O‘rtacha")),
        ("major", _("Jiddiy")),
        ("critical", _("Favqulodda")),
    )
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
    NOTIFICATION_TYPE = (
        ("maintenance_due", _("Texnik xizmat muddati yaqinlashmoqda")),
        ("maintenance_completed", _("Texnik xizmat bajarildi")),
        ("fault_reported", _("Nosozlik aniqlandi")),
        ("fault_resolved", _("Nosozlik bartaraf etildi")),
        ("system", _("Tizim xabarnomasi")),
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
