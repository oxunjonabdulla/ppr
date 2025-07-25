# Generated by Django 5.1.7 on 2025-06-24 07:12

from django.db import migrations, models

import apps.utils.get_upload_path


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=255, verbose_name="Korxona nomi")),
                (
                    "code",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Korxona maxsus kodi"
                    ),
                ),
                ("address", models.TextField(blank=True, verbose_name="Manzil")),
                (
                    "contact_email",
                    models.EmailField(
                        blank=True,
                        max_length=254,
                        verbose_name="Aloqa elektron pochtasi",
                    ),
                ),
                (
                    "contact_phone",
                    models.CharField(
                        blank=True, max_length=15, verbose_name="Aloqa telefoni"
                    ),
                ),
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=apps.utils.get_upload_path.get_upload_path,
                        verbose_name="Korxona logosi",
                    ),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="Faol")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Korxona",
                "verbose_name_plural": "Korxonalar",
            },
        ),
    ]
