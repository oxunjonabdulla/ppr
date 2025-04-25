from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.get_upload_path import get_upload_path

#  Ta'mirlash jadvali
# ------------------------------------------------------------------------------------------


class MaintenanceSchedule(models.Model):
    MAINTENANCE_TITLE_CHOICES = (
        # Tokarlik dastgohlari
        ("lathe_inspection", _("Tokarlik dastgohlari jadvali")),
        ("lathe_check", _("Texnik ko'rik sanasi")),
        ("lathe_next_check", _("Keyingi texnik ko‘rik sanasi")),
        # Payvandlash uskunalari
        ("welding_inspection", _("Payvandlash uskunalari jadvali")),
        ("welding_check", _("Texnik ko'rik sanasi")),
        ("welding_next_check", _("Keyingi texnik ko‘rik sanasi")),
        ("voltmeter_check", _("Voltmetr ko‘rik sanasi")),
        ("voltmeter_next_check", _("Keyingi voltmetr ko‘rik sanasi")),
        # Isitish qozoni
        ("boiler_schedule", _("Isitish qozoni jadvali")),
        ("boiler_inner_outer", _("Tashqi va ichki ko‘rik sanasi")),
        (
            "boiler_next_inner_outer",
            _("Keyingi tashqi va ichki ko‘rik sanasi"),
        ),
        ("boiler_flush_test", _("Yuvish va sinovdan o‘tkazish sanasi")),
        (
            "boiler_next_flush_test",
            _("Keyingi yuvish va sinovdan o‘tkazish sanasi"),
        ),
        ("boiler_manometer", _("Manometrlarni qiyoslash sanasi")),
        ("boiler_next_manometer", _("Keyingi manometrlarni qiyoslash sanasi")),
        # Yuk ko'taruvchi kranlar
        ("crane_schedule", _("Yuk ko'taruvchi kranlar jadvali")),
        ("crane_full_inspection", _("To‘liq texnik ko‘rik sanasi")),
        ("crane_next_full", _("Keyingi to‘liq texnik ko‘rik sanasi")),
        ("crane_partial", _("Qisman texnik ko‘rik sanasi")),
        ("crane_next_partial", _("Keyingi qisman texnik ko‘rik sanasi")),
        ("crane_lab_test", _("Laboratoriya tekshiruvi sanasi")),
        ("crane_next_lab_test", _("Keyingi laboratoriya tekshiruvi sanasi")),
        ("crane_leveling", _("Nivelirovka sanasi")),
        ("crane_next_leveling", _("Keyingi nivelirovka sanasi")),
        # Bosim ostida sig'imlar
        ("pressure_schedule", _("Bosim ostida sig'imlar jadvali")),
        ("pressure_inner", _("Ichki ko‘rik sanasi")),
        ("pressure_next_inner", _("Keyingi ichki ko‘rik sanasi")),
        ("pressure_hydro_test", _("Gidravlik sinov sanasi")),
        ("pressure_next_hydro_test", _("Keyingi gidravlik sinov sanasi")),
        ("pressure_valve", _("Ortiqcha bosimdan saqlovchi qurilma sanasi")),
        (
            "pressure_next_valve",
            _("Keyingi ortiqcha bosimdan saqlovchi qurilma sanasi"),
        ),
        ("pressure_manometer", _("Manometrlarni qiyoslash sanasi")),
        (
            "pressure_next_manometer",
            _("Keyingi manometrlarni qiyoslash sanasi"),
        ),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    title = models.CharField(
        _("Xizmat turi"), max_length=100, choices=MAINTENANCE_TITLE_CHOICES
    )
    description = models.TextField(_("Ta'rif"), blank=True)

    scheduled_date = models.DateField(
        _("Rejalashtirilgan sana"), null=True, blank=True
    )
    estimated_duration = models.PositiveIntegerField(
        _("Taxminiy muddat (kun)"), null=True, blank=True
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
        return f"{self.get_title_display()} - {self.scheduled_date}"


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
