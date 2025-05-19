from rest_framework import serializers

from apps.maintenance.models import MaintenanceSchedule, MaintenanceWarning, EquipmentFault


class MaintenanceScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceSchedule
        # exclude = ["equipment__type"]
        fields = "__all__"
        read_only_fields = [
            "next_maintenance_date",  # calculated automatically in save()
            "created_at",
            "updated_at", ]


class MaintenanceWarningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceWarning
        fields = "__all__"


class EquipmentFaultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFault
        fields = "__all__"