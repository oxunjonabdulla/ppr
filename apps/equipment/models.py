from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import User
from apps.utils.get_upload_path import get_upload_path

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
    manufacture_date = models.DateField(
        _("Ishlab chiqarilgan yili"), null=True, blank=True
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
    is_conserved = models.BooleanField(
        default=False, verbose_name="Konservatsiyaga olish"
    )
    conservation_reason = models.TextField(
        blank=True, null=True, verbose_name="Konservatsiya sababi"
    )
    notes = models.TextField(blank=True, null=True, verbose_name="Tavsiyalar")
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lathe_machine_author",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaratilgan vaqti"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("O'zgartirilgan vaqti"), auto_now=True
    )

    class Meta:
        verbose_name = "Tokarlik dastgohi"
        verbose_name_plural = "Tokarlik dastgohlari"


# Payvandlash uskunalari
# ------------------------------------------------------------------------------------------
class WeldingEquipment(AbstractBaseEquipment):
    is_conserved = models.BooleanField(
        default=False, verbose_name="Konservatsiyaga olish"
    )
    conservation_reason = models.TextField(
        blank=True, null=True, verbose_name="Konservatsiya sababi"
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="welding_equipment_author",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaratilgan vaqti"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("O'zgartirilgan vaqti"), auto_now=True
    )

    class Meta:
        verbose_name = "Payvandlash qurilmasi"
        verbose_name_plural = "Payvandlash qurilmalari"


# Isitish qozoni
# ------------------------------------------------------------------------------------------
class HeatingBoiler(AbstractBaseEquipment):
    fuel_type = models.CharField(
        max_length=100, verbose_name="Yoqilg‘i turi", blank=True
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="heating_boiler_author",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaratilgan vaqti"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("O'zgartirilgan vaqti"), auto_now=True
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
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="lifting_crane_author",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaratilgan vaqti"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("O'zgartirilgan vaqti"), auto_now=True
    )

    class Meta:
        verbose_name = "Yuk ko'tarish krani"
        verbose_name_plural = "Yuk ko'tarish kranlari"

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"


# Bosim ostida sig'imlar
# -----------------------------------------------------------------------------------------
class PressureVessel(AbstractBaseEquipment):
    category_name = models.CharField(
        max_length=100, verbose_name="Sig‘imning kategoriyasi", blank=True
    )
    author = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="pressure_vessel_author",
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaratilgan vaqti"), auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("O'zgartirilgan vaqti"), auto_now=True
    )

    class Meta:
        verbose_name = "Bosim ostida sig'im"
        verbose_name_plural = "Bosim ostida sig'imlar"

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"
