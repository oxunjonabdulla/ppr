import uuid
from io import BytesIO

import qrcode
from django.conf import settings
from django.core.files import File


def generate_equipment_qr_code(
    equipment_instance, base_url="https://api.ppr.vchdqarshi.uz/api"
):
    """
    Generate QR code for equipment instance
    """
    # Determine the URL based on equipment type
    if hasattr(equipment_instance, "AUTO_TYPE"):
        equipment_type = equipment_instance.AUTO_TYPE.replace("_", "-")
        url = f"{base_url}/{equipment_type}-detail/{equipment_instance.pk}/"
    else:
        url = f"{base_url}/equipment-detail/{equipment_instance.pk}/"

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create image
    qr_image = qr.make_image(fill_color="black", back_color="white")

    # Save to BytesIO
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer, url
