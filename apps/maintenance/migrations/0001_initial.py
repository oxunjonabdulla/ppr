# Generated by Django 5.1.7 on 2025-06-24 07:12

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.utils.get_upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("equipment", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MaintenanceSchedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "maintenance_type",
                    models.CharField(
                        choices=[
                            ("inspection", "Texnik ko'rik"),
                            ("full_inspection", "To'liq texnik ko'rik"),
                            ("partial_inspection", "Qisman texnik ko'rik"),
                            ("voltmeter_check", "Voltmetr tekshiruvi"),
                            ("manometer_check", "Manometr tekshiruvi"),
                            ("hydraulic_test", "Gidravlik sinov"),
                            ("pressure_test", "Bosim sinovi"),
                            ("flush_test", "Yuvish va sinov"),
                            ("inner_outer_check", "Ichki/tashqi tekshiruv"),
                            ("lab_test", "Laboratoriya tekshiruvi"),
                            ("leveling_check", "Nivelirovka tekshiruvi"),
                            ("safety_valve_check", "Xavfsizlik klapani tekshiruvi"),
                            ("lubrication_check", "Yog'lash tekshiruvi"),
                            ("alignment_check", "Markalash tekshiruvi"),
                            ("calibration_check", "Kalibrlash tekshiruvi"),
                        ],
                        max_length=50,
                        verbose_name="Texnik xizmat turi",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Ta'rif")),
                (
                    "scheduled_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Ko'rik sanasi"
                    ),
                ),
                (
                    "next_maintenance_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Keyingi ko'rik sanasi"
                    ),
                ),
                (
                    "is_completed",
                    models.BooleanField(default=False, verbose_name="Bajarildi"),
                ),
                (
                    "completed_date",
                    models.DateField(
                        blank=True, null=True, verbose_name="Bajarilgan sana"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="MaintenanceWarning",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "warning_level",
                    models.CharField(
                        choices=[
                            ("low", "Past"),
                            ("medium", "O‘rta"),
                            ("high", "Yuqori"),
                            ("critical", "Favqulodda"),
                        ],
                        default="medium",
                        max_length=15,
                        verbose_name="Ogohlantirish darajasi",
                    ),
                ),
                (
                    "warning_time",
                    models.CharField(
                        choices=[
                            ("one_month", "1 oy oldin"),
                            ("fifteen_days", "15 kun oldin"),
                            ("seven_days", "7 kun oldin"),
                            ("three_days", "3 kun oldin"),
                        ],
                        max_length=20,
                        verbose_name="Ogohlantirish vaqti",
                    ),
                ),
                (
                    "message",
                    models.TextField(blank=True, verbose_name="Ogohlantirish xabari"),
                ),
                (
                    "is_sent",
                    models.BooleanField(default=False, verbose_name="Yuborildi"),
                ),
                (
                    "sent_date",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Yuborilgan sana"
                    ),
                ),
                (
                    "sent_to_telegram",
                    models.BooleanField(
                        default=False, verbose_name="Telegramga yuborilgan"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Maintenance Warning",
                "verbose_name_plural": "Maintenance Warnings",
            },
        ),
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Xabarnoma sarlavhasi"
                    ),
                ),
                (
                    "message",
                    models.TextField(blank=True, verbose_name="Xabarnoma matni"),
                ),
                (
                    "notification_type",
                    models.CharField(
                        choices=[
                            ("maintenance_due", "Texnik xizmat muddati yaqinlashmoqda"),
                            ("maintenance_completed", "Texnik xizmat bajarildi"),
                            ("fault_reported", "Nosozlik aniqlandi"),
                            ("fault_resolved", "Nosozlik bartaraf etildi"),
                            ("system", "Tizim xabarnomasi"),
                        ],
                        default="maintenance_due",
                        max_length=25,
                        verbose_name="Xabarnoma turi",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "is_read",
                    models.BooleanField(default=False, verbose_name="O‘qilgan"),
                ),
                (
                    "read_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="O‘qilgan vaqti"
                    ),
                ),
                (
                    "sent_to_telegram",
                    models.BooleanField(
                        default=False, verbose_name="Telegramga yuborilgan"
                    ),
                ),
            ],
            options={
                "verbose_name": "Xabarnoma",
                "verbose_name_plural": "Xabarnomalar",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="EquipmentFault",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Nosozlik nomi"
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Ta'rifi")),
                (
                    "severity",
                    models.CharField(
                        choices=[
                            ("minor", "Yengil"),
                            ("moderate", "O‘rtacha"),
                            ("major", "Jiddiy"),
                            ("critical", "Favqulodda"),
                        ],
                        default="moderate",
                        max_length=10,
                        verbose_name="Holati",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        upload_to=apps.utils.get_upload_path.get_upload_path,
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg", "jpeg", "png", "heic"]
                            )
                        ],
                        verbose_name="Rasmi",
                    ),
                ),
                (
                    "capture_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Suratga olish vaqti"
                    ),
                ),
                (
                    "reported_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Xabar berilgan vaqti"
                    ),
                ),
                (
                    "is_resolved",
                    models.BooleanField(default=False, verbose_name="Yechilgan"),
                ),
                (
                    "resolved_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Hal qilingan vaqt"
                    ),
                ),
                (
                    "resolution_notes",
                    models.TextField(blank=True, verbose_name="Nosozlik haqida izoh"),
                ),
                (
                    "gps_location",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="GPS location",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "equipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="faults",
                        to="equipment.equipment",
                        verbose_name="Uskuna",
                    ),
                ),
            ],
            options={
                "verbose_name": "Uskunalar nosozligi",
                "verbose_name_plural": "Uskunalar nosozliklari",
            },
        ),
    ]
