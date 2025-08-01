import uuid
from io import BytesIO

import qrcode
from django.core.files import File
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
    qr_code = models.ImageField(
        _("QR Kod"),
        upload_to="qr_codes/",
        null=True,
        blank=True,
        help_text=_("QR kod avtomatik yaratiladi"),
    )
    latitude = models.DecimalField(
        _("Kenglik"),
        max_digits=10,
        decimal_places=8,
        null=True,
        blank=True,
        help_text=_("Joylashuv kengligi"),
    )
    longitude = models.DecimalField(
        _("Uzunlik"),
        max_digits=11,
        decimal_places=8,
        null=True,
        blank=True,
        help_text=_("Joylashuv uzunligi"),
    )
    location_address = models.CharField(
        _("Manzil"),
        max_length=500,
        blank=True,
        help_text=_("Joylashuv manzili"),
    )

    class Meta:
        abstract = True

    def generate_qr_code(self, url):
        """Generate QR code for the equipment"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Create QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save to BytesIO
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        buffer.seek(0)

        # Generate filename
        filename = (
            f"qr_{self.__class__.__name__.lower()}_{uuid.uuid4().hex[:8]}.png"
        )

        # Save to model field
        self.qr_code.save(filename, File(buffer), save=False)
        buffer.close()


# Equipment Base Model
# -----------------------------------------------------------------------------------------


class Equipment(models.Model):
    LATHE_MACHINE = _("Tokarlik dastgohi")
    WELDING_EQUIPMENT = _("Payvandlash uskunalari")
    HEATING_BOILER = _("Isitish qozoni")
    PRESSURE_VESSEL = _("Yuk ko'taruvchi kranlar")
    LIFTING_CRANE = _("Bosim ostida sig'imlar")

    EQUIPMENT_MODEL_CHOICES = [
        ("lathe_machine", LATHE_MACHINE),
        ("welding_equipment", WELDING_EQUIPMENT),
        ("heating_boiler", HEATING_BOILER),
        ("pressure_vessel", PRESSURE_VESSEL),
        ("lifting_crane", LIFTING_CRANE),
    ]

    type = models.CharField(max_length=100, choices=EQUIPMENT_MODEL_CHOICES)

    def __str__(self):
        if self.type == "lathe_machine":
            try:
                return str(self.lathemachine.detail_name)
            except LatheMachine.DoesNotExist:
                return self.get_type_display()
        elif self.type == "welding_equipment":
            try:
                return str(self.weldingequipment.detail_name)
            except WeldingEquipment.DoesNotExist:
                return self.get_type_display()
        elif self.type == "heating_boiler":
            try:
                return str(self.heatingboiler.detail_name)
            except HeatingBoiler.DoesNotExist:
                return self.get_type_display()
        elif self.type == "pressure_vessel":
            try:
                return str(self.pressurevessel.detail_name)
            except PressureVessel.DoesNotExist:
                return self.get_type_display()
        elif self.type == "lifting_crane":
            try:
                return str(self.liftingcrane.detail_name)
            except LiftingCrane.DoesNotExist:
                return self.get_type_display()
        else:
            return self.get_type_display()

    def get_real_instance(self):
        if self.type == "lathe_machine":
            return self.lathemachine
        elif self.type == "welding_equipment":
            return self.weldingequipment
        elif self.type == "heating_boiler":
            return self.heatingboiler
        elif self.type == "lifting_crane":
            return self.liftingcrane
        elif self.type == "pressure_vessel":
            return self.pressurevessel
        return self


# Tokarlik dastgohlari
# ------------------------------------------------------------------------------------------------
class LatheMachine(AbstractBaseEquipment, Equipment):
    AUTO_TYPE = "lathe_machine"
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

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"

    def save(self, *args, **kwargs):
        self.type = self.AUTO_TYPE
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.qr_code:
            detail_url = f"https://api.ppr.vchdqarshi.uz/api/lathe_machine-detail/{self.pk}/"
            self.generate_qr_code(detail_url)
            # Save again to update QR code field
            super().save(update_fields=["qr_code"])

    def get_location_display(self):
        """Get formatted location string"""
        if self.latitude and self.longitude:
            return f"{self.latitude}, {self.longitude}"
        return "Joylashuv belgilanmagan"


# Payvandlash uskunalari
# ------------------------------------------------------------------------------------------
class WeldingEquipment(AbstractBaseEquipment, Equipment):
    AUTO_TYPE = "welding_equipment"
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

    def __str__(self):
        return f"{self.detail_name} - {self.factory_number}"

    def save(self, *args, **kwargs):
        self.type = self.AUTO_TYPE
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.qr_code:
            detail_url = f"https://api.ppr.vchdqarshi.uz/api/welding_equipment-detail/{self.pk}/"
            self.generate_qr_code(detail_url)
            # Save again to update QR code field
            super().save(update_fields=["qr_code"])


# Isitish qozoni
# ------------------------------------------------------------------------------------------
class HeatingBoiler(AbstractBaseEquipment, Equipment):
    AUTO_TYPE = "heating_boiler"
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

    def save(self, *args, **kwargs):
        self.type = self.AUTO_TYPE
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or not self.qr_code:
            detail_url = f"https://api.ppr.vchdqarshi.uz/api/heating_boiler-detail/{self.pk}/"
            self.generate_qr_code(detail_url)
            # Save again to update QR code field
            super().save(update_fields=["qr_code"])


# Yuk ko'taruvchi kranlar
# ------------------------------------------------------------------------------------------
class LiftingCrane(AbstractBaseEquipment, Equipment):
    AUTO_TYPE = "lifting_crane"
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

    def save(self, *args, **kwargs):
        self.type = self.AUTO_TYPE
        super().save(*args, **kwargs)
        is_new = self.pk is None

        if is_new or not self.qr_code:
            detail_url = f"https://api.ppr.vchdqarshi.uz/api/lifting_crane-detail/{self.pk}/"
            self.generate_qr_code(detail_url)
            # Save again to update QR code field
            super().save(update_fields=["qr_code"])


# Bosim ostida sig'imlar
# -----------------------------------------------------------------------------------------
class PressureVessel(AbstractBaseEquipment, Equipment):
    AUTO_TYPE = "pressure_vessel"
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

    def save(self, *args, **kwargs):
        self.type = self.AUTO_TYPE
        super().save(*args, **kwargs)
        is_new = self.pk is None

        if is_new or not self.qr_code:
            detail_url = f"https://api.ppr.vchdqarshi.uz/api/pressure_vessel-detail/{self.pk}/"
            self.generate_qr_code(detail_url)
            # Save again to update QR code field
            super().save(update_fields=["qr_code"])
