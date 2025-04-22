from django.contrib import admin

from apps.equipment.models import (
    HeatingBoiler,
    LatheMachine,
    LiftingCrane,
    PressureVessel,
    WeldingEquipment,
)

admin.site.register(
    [
        WeldingEquipment,
        LiftingCrane,
        HeatingBoiler,
        PressureVessel,
        LatheMachine,
    ]
)
