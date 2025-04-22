from django.contrib import admin

from .models import (
    EquipmentFault,
    MaintenanceSchedule,
    MaintenanceWarning,
    Notification,
)

admin.site.register(
    [MaintenanceSchedule, MaintenanceWarning, EquipmentFault, Notification]
)
