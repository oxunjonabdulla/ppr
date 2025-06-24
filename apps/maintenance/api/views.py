from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from apps.maintenance.models import (
    EquipmentFault,
    MaintenanceSchedule,
    MaintenanceWarning,
)
from apps.users.api.permissions import IsEquipmentMaster, IsEquipmentOperator
from apps.utils.paginator import (  # Assuming you have this
    StandardResultsSetPagination,
)

from .serializers import (
    EquipmentFaultModelSerializer,
    MaintenanceScheduleModelSerializer,
    MaintenanceWarningModelSerializer,
)


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Ta'mirlash jadvali"])
class MaintenanceScheduleListCreateAPIView(generics.ListCreateAPIView):
    queryset = MaintenanceSchedule.objects.order_by("-created_at")
    serializer_class = MaintenanceScheduleModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
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


@extend_schema(tags=["Ta'mirlash jadvali"])
class MaintenanceScheduleRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = MaintenanceSchedule.objects.all()
    serializer_class = MaintenanceScheduleModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = MaintenanceSchedule.objects.get(pk=self.kwargs["pk"])
            return instance
        except MaintenanceSchedule.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos ta'mirlash jadvali mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )


#  MaintenanceWarnings
#  -----------------------------------------------------------------------------


@extend_schema(tags=["Ta'mirlash ogohlantirishlari"])
class MaintenanceWarningListAPIView(ListAPIView):
    queryset = MaintenanceWarning.objects.order_by("-sent_date")
    serializer_class = MaintenanceWarningModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["sent_date", "warning_level", "warning_time"]
    pagination_class = StandardResultsSetPagination


@extend_schema(tags=["Ta'mirlash ogohlantirishlari"])
class MaintenanceWarningRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = MaintenanceWarning.objects.all()
    serializer_class = MaintenanceWarningModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = MaintenanceWarning.objects.get(pk=self.kwargs["pk"])
            return instance
        except MaintenanceWarning.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos ta'mirlash ogohlantirishlari mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )


#  EquipmentFault
#  -----------------------------------------------------------------------------


@extend_schema(tags=["Uskunalar nosozligi"])
class EquipmentFaultListCreateAPIView(ListCreateAPIView):
    queryset = EquipmentFault.objects.order_by("-created_at")
    serializer_class = EquipmentFaultModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentOperator]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "equipment", "severity"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data={"status": status.HTTP_201_CREATED, "data": serializer.data},
            headers=headers,
        )
