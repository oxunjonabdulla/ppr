from rest_framework import serializers

from apps.equipment.api.serializers import EquipmentPolymorphicSerializer
from apps.equipment.models import Equipment
from apps.maintenance.models import (
    EquipmentFault,
    MaintenanceSchedule,
    MaintenanceWarning,
)
from apps.users.api.serializers import UserSerializer


class MaintenanceScheduleModelSerializer(serializers.ModelSerializer):
    equipment_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipment.objects.all(), source="equipment", write_only=True
    )
    equipment = EquipmentPolymorphicSerializer(read_only=True)

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

    assigned_to = MinimalUserSerializer()
    completed_by = MinimalUserSerializer()

    class Meta:
        model = MaintenanceSchedule
        # exclude = ["equipment__type"]
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]


class MaintenanceWarningModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceWarning
        fields = "__all__"


class EquipmentFaultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentFault
        fields = "__all__"
