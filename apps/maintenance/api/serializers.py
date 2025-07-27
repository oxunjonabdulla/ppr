from rest_framework import serializers

from apps.equipment.api.serializers import EquipmentPolymorphicSerializer
from apps.maintenance.models import (
    EquipmentFault,
    MaintenanceSchedule,
    MaintenanceWarning,
)


class MaintenanceScheduleModelSerializer(serializers.ModelSerializer):
    equipment = EquipmentPolymorphicSerializer(read_only=True)

    class Meta:
        model = MaintenanceSchedule
        # exclude = ["equipment__type"]
        fields = "__all__"
        read_only_fields = [
            "next_maintenance_date",  # calculated automatically in save()
            "created_at",
            "updated_at",
        ]


class MaintenanceWarningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceWarning
        fields = "__all__"


class EquipmentFaultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFault
        fields = "__all__"
