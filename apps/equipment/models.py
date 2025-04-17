from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.utils.get_upload_path import get_upload_path


# Uskunalar kategoriyasi
# ------------------------------------------------------------------------------------------
class EquipmentCategory(models.Model):
    """
    Categories for different types of equipment (e.g, Lathes,Welding devices, Lifting cranes,
     Capacities under pressure,Heating boilers)
    """

    name = models.CharField(_("Kategoriya nomi"), max_length=255)
    description = models.CharField(_("Izoh"), blank=True)
    image = models.ImageField(
        _("Korxona logosi"), upload_to=get_upload_path, null=True, blank=True
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="equipment_categories",
    )

    class Meta:
        verbose_name = _("Uskunalar kategoriyalari")
        verbose_name_plural = _("Uskunalar kategoriyalari")
        constraints = [
            models.UniqueConstraint(
                fields=["name", "company"], name="unique_equipment_category"
            )
        ]

    def __str__(self):
        return f"Kategoriyasi: {self.name}, Korxona: ({self.company.name})"


# AbstractBaseEquipment model
# ------------------------------------------------------------------------------------------
class AbstractBaseEquipment(models.Model):
    image = models.ImageField(
        _("Rasm"), upload_to=get_upload_path, null=True, blank=True
    )
    company_name = models.CharField(
        _("Korxona nomi"), max_length=255, blank=True
    )
    detail_name = models.CharField(_("Detal nomi"), max_length=255, blank=True)
    manufacture_date = models.CharField(
        _("Ishlab chiqarilgan yili"), blank=True
    )
    factory_number = models.CharField(
        _("Zavod raqami"), max_length=255, blank=True
    )
    registration_number = models.CharField(
        _("Qayd raqami"), max_length=255, blank=True
    )
    installation_location = models.CharField(
        _("O‘rnatilgan joyi"), max_length=255, blank=True
    )
    technical_condition = models.CharField(
        _("Texnik holati"),
        max_length=50,
        choices=[("working", "Soz"), ("faulty", "Nosoz")],
        default="working",
        blank=True,
    )
    responsible_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Javobgar shaxs"),
    )

    class Meta:
        abstract = True


# Tokarlik dastgohlari
# ------------------------------------------------------------------------------------------
class LatheMachine(AbstractBaseEquipment):
    last_maintenance = models.DateField(
        verbose_name="Texnik ko'rik sanasi", null=True, blank=True
    )
    next_maintenance = models.DateField(
        blank=True, null=True, verbose_name="Keyingi texnik ko‘rik sanasi"
    )
    is_conserved = models.BooleanField(
        default=False, verbose_name="Konservatsiyaga olish"
    )
    conservation_reason = models.TextField(
        blank=True, null=True, verbose_name="Konservatsiya sababi"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Tavsiyalar")

    class Meta:
        verbose_name = "Tokarlik dastgohi"
        verbose_name_plural = "Tokarlik dastgohlari"

    def save(self, *args, **kwargs):
        if self.last_maintenance and not self.next_maintenance:
            self.next_maintenance = self.last_maintenance + timedelta(days=365)

        super().save(*args, **kwargs)


# Payvandlash uskunalari
# ------------------------------------------------------------------------------------------
class WeldingEquipment(AbstractBaseEquipment):
    last_maintenance = models.DateField(
        verbose_name="Texnik ko'rik sanasi", null=True, blank=True
    )
    next_maintenance = models.DateField(
        blank=True, null=True, verbose_name="Keyingi texnik ko‘rik sanasi"
    )
    is_conserved = models.BooleanField(
        default=False, verbose_name="Konservatsiyaga olish"
    )
    conservation_reason = models.TextField(
        blank=True, null=True, verbose_name="Konservatsiya sababi"
    )
    voltmeter_inspection_date = models.DateField(
        blank=True, null=True, verbose_name="Voltmetr ko‘rik sanasi"
    )

    class Meta:
        verbose_name = "Payvandlash qurilmasi"
        verbose_name_plural = "Payvandlash qurilmalari"

    def save(self, *args, **kwargs):
        if self.last_maintenance and not self.next_maintenance:
            self.next_maintenance = self.last_maintenance + timedelta(days=365)
        super().save(*args, **kwargs)


# Isitish qozoni
# ------------------------------------------------------------------------------------------
class HeatingBoiler(AbstractBaseEquipment):
    external_internal_inspection_date = models.DateField(
        verbose_name="Tashqi va ichki ko‘rik sanasi", blank=True
    )
    washing_testing_date = models.DateField(
        verbose_name="Yuvish va sinovdan o‘tkazish sanasi",
        blank=True,
        null=True,
    )
    manometer_calibration_date = models.DateField(
        verbose_name="Manometrlarni qiyoslash sanasi", blank=True, null=True
    )
    fuel_type = models.CharField(
        max_length=100, verbose_name="Yoqilg‘i turi", blank=True
    )

    class Meta:
        verbose_name = "Isitish qozoni"
        verbose_name_plural = "Isitish qozonlari"

    def __str__(self):
        return f"{self.detail_name} ({self.factory_number})"


# Yuk ko'taruvchi kranlar
# ------------------------------------------------------------------------------------------
class LiftingCrane(AbstractBaseEquipment):
    under_crane_path_length = models.CharField(
        max_length=100, verbose_name="Kran osti yo‘li uzunligi"
    )
    crane_width_length = models.CharField(
        max_length=100, verbose_name="Kran eni uzunligi"
    )

    full_inspection_date = models.DateField(
        verbose_name=_("To‘liq texnik ko‘rik sanasi"), null=True, blank=True
    )
    partial_inspection_date = models.DateField(
        verbose_name=_("Qisman texnik ko‘rik sanasi"), null=True, blank=True
    )
    next_full_inspection_date = models.DateField(
        verbose_name=_("Keyingi to‘liq texnik ko‘rik sanasi"),
        null=True,
        blank=True,
    )
    next_lab_test_date = models.DateField(
        verbose_name=_("Keyingi laboratoriya tekshiruvi sanasi"),
        null=True,
        blank=True,
    )
    next_leveling_date = models.DateField(
        verbose_name=_("Keyingi nivelirovka sanasi"), null=True, blank=True
    )

    class Meta:
        verbose_name = "Yuk ko'tarish krani"
        verbose_name_plural = "Yuk ko'tarish kranlari"

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"


# Bosim ostida sig'imlar
# ------------------------------------------------------------------------------------------


class PressureVessel(AbstractBaseEquipment):
    internal_inspection_date = models.DateField(
        verbose_name="Ichki ko‘rik sanasi", blank=True, null=True
    )
    hydraulic_test_date = models.DateField(
        verbose_name="Gidravlik sinov sanasi", blank=True, null=True
    )
    overpressure_protection_check_date = models.DateField(
        verbose_name="Ortiqcha bosimdan saqlovchi qurilma sanasi",
        blank=True,
        null=True,
    )
    manometer_calibration_date = models.DateField(
        verbose_name="Manometrlarni qiyoslash sanasi", blank=True, null=True
    )
    next_internal_inspection_date = models.DateField(
        verbose_name="Keyingi ichki ko‘rik sanasi", blank=True, null=True
    )
    next_hydraulic_test_date = models.DateField(
        verbose_name="Keyingi gidravlik sinov sanasi", blank=True, null=True
    )
    category_name = models.CharField(
        max_length=100, verbose_name="Kategoriya nomi", blank=True
    )

    class Meta:
        verbose_name = "Bosim ostida sig'im"
        verbose_name_plural = "Bosim ostida sig'imlar"

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"
