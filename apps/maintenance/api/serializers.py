from rest_framework import serializers

from apps.maintenance.models import MaintenanceSchedule


class MaintenanceScheduleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceSchedule
        fields = [
            "id",
            "content_type",
            "object_id",
            "maintenance_type",
            "description",
            "scheduled_date",
            "estimated_unit",
            "estimated_value",
            "next_maintenance_date",
            "assigned_to",
            "is_completed",
            "completed_date",
            "completed_by",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "next_maintenance_date",  # calculated automatically in save()
            "created_at",
            "updated_at",
        ]
