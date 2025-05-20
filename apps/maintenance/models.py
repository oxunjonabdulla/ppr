from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image
from rest_framework.exceptions import ValidationError

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
    equipment = models.ForeignKey(
        "equipment.Equipment",
        on_delete=models.CASCADE,
        verbose_name=_("Uskuna"),
        related_name="maintenance_schedules",
    )
    maintenance_type = models.CharField(
        _("Texnik xizmat turi"),
        max_length=50,
        choices=MAINTENANCE_TYPE_CHOICES,
    )
    description = models.TextField(_("Ta'rif"), blank=True)
    scheduled_date = models.DateField(
        _("Ko'rik sanasi"), null=True, blank=True
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    def calculate_days_until_next_maintenance(self):
        """
        This method calculates the days remaining until the next maintenance.
        If the next maintenance date is in the future, it returns the number of days.
        If it's in the past, it returns a negative value.
        """
        if self.maintenance_schedule.next_maintenance_date:
            return (
                self.maintenance_schedule.next_maintenance_date
                - timezone.now().date()
            ).days
        return None

    def set_warning_time(self):
        """
        This method determines the warning time based on the remaining days.
        It assigns a warning time based on predefined intervals.
        """
        days_left = self.calculate_days_until_next_maintenance()

        if days_left is not None:
            if days_left <= 3:
                self.warning_time = "three_days"
                self.warning_level = "critical"
            elif days_left <= 7:
                self.warning_time = "seven_days"
                self.warning_level = "high"
            elif days_left <= 15:
                self.warning_time = "fifteen_days"
                self.warning_level = "medium"
            elif days_left <= 30:
                self.warning_time = "one_month"
                self.warning_level = "low"
            else:
                self.warning_time = None
                self.message = ""
                return
                # Set the message

            self.message = f"{str(self.maintenance_schedule.equipment).capitalize()} ning texnik ko‘rikga {days_left} kun qoldi. ({self.maintenance_schedule.next_maintenance_date})"
        else:
            self.warning_time = None
            self.message = ""

        # Uskuna nosozligi


# ------------------------------------------------------------------------------------------
class EquipmentFault(models.Model):
    FAULT_SEVERITY = (
        ("minor", _("Yengil")),
        ("moderate", _("O‘rtacha")),
        ("major", _("Jiddiy")),
        ("critical", _("Favqulodda")),
    )
    equipment = models.ForeignKey(
        "equipment.Equipment",
        on_delete=models.CASCADE,
        verbose_name=_("Uskuna"),
        related_name="faults",
    )
    title = models.CharField(_("Nosozlik nomi"), max_length=255, blank=True)
    description = models.TextField(_("Ta'rifi"), blank=True)
    severity = models.CharField(
        _("Holati"), max_length=10, choices=FAULT_SEVERITY, default="moderate"
    )
    photo = models.ImageField(
        _("Rasmi"),
        upload_to=get_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "jpeg", "png", "heic"]
            )
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Uskunalar nosozligi")
        verbose_name_plural = _("Uskunalar nosozliklari")

    def __str__(self):
        return f"{self.title} - {self.equipment}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.photo.path)
        max_width = 800
        max_height = 600
        if img.width > max_width or img.height > max_height:
            new_size = (max_width, max_height)
            img.thumbnail(new_size, Image.Resampling.LANCZOS)
            img.save(self.photo.path)

        if self.pk:
            old = EquipmentFault.objects.get(pk=self.pk)
            if old.photo and self.photo != old.photo:
                raise ValidationError(
                    "You cannot change the photo after submission."
                )
        super().save(*args, **kwargs)


@receiver(post_delete, sender=EquipmentFault)
def delete_fault_photo(sender, instance, **kwargs):
    if instance.photo:
        instance.photo.delete(save=False)


@receiver(pre_save, sender=EquipmentFault)
def delete_old_fault_photo(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if instance.photo != old_instance.photo:
                if old_instance.photo:
                    old_instance.photo.delete(save=False)
        except sender.DoesNotExist:
            pass


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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
