from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.response import Response

from apps.maintenance.models import MaintenanceSchedule
from apps.users.api.permissions import IsEquipmentMaster
from apps.utils.paginator import StandardResultsSetPagination  # Assuming you have this

from .serializers import MaintenanceScheduleModelSerializer


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Ta'mirlash jadvali"])
class MaintenanceScheduleListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaintenanceSchedule.objects.order_by("-created_at")
    serializer_class = MaintenanceScheduleModelSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsEquipmentMaster,
    ]  # You can add custom permissions
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["maintenance_type", "description"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": status.HTTP_201_CREATED, "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
