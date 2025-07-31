import uuid
from io import BytesIO

from django.core.files import File
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.equipment.api.serializers import (
    HeatingBoilerModelSerializer,
    LatheMachineModelSerializers,
    LiftingCraneModelSerializer,
    PressureVesselModelSerializer,
    WeldingEquipmentModelSerializer,
)
from apps.equipment.models import (
    HeatingBoiler,
    LatheMachine,
    LiftingCrane,
    PressureVessel,
    WeldingEquipment,
)
from apps.users.api.permissions import IsEquipmentMaster
from apps.utils.paginator import StandardResultsSetPagination
from apps.utils.qr_code import generate_equipment_qr_code


# Tokarlik dastgohlari
# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Tokarlik dastgohlari"])
class LatheMachineListCreateAPIView(generics.ListCreateAPIView):
    queryset = LatheMachine.objects.order_by("-created_at")
    serializer_class = LatheMachineModelSerializers
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "detail_name"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        """Save the instance and generate QR code"""
        instance = serializer.save(author=self.request.user)

        # QR code is generated automatically in the model's save method
        # But we can also trigger it manually if needed
        if not instance.qr_code:
            buffer, url = generate_equipment_qr_code(instance)
            filename = f"qr_lathe_{instance.pk}_{uuid.uuid4().hex[:8]}.png"
            instance.qr_code.save(filename, File(buffer), save=True)
            buffer.close()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Tokarlik dastgohi muvaffaqiyatli yaratildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        """Add request to serializer context for URL building"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Tokarlik dastgohlari"])
class LatheMachineRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = LatheMachine.objects.all()
    serializer_class = LatheMachineModelSerializers
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = LatheMachine.objects.get(pk=self.kwargs["pk"])
            return instance
        except LatheMachine.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos tokarlik dastgohi mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_204_NO_CONTENT, "data": serializer.data}
        )


# Payvandlash uskunalari
# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Payvandlash qurilmalari"])
class WeldingEquipmentListCreateAPIView(generics.ListCreateAPIView):
    queryset = WeldingEquipment.objects.order_by("-created_at")
    serializer_class = WeldingEquipmentModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "detail_name"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        """Save the instance and generate QR code"""
        instance = serializer.save(author=self.request.user)

        # QR code is generated automatically in the model's save method
        # But we can also trigger it manually if needed
        if not instance.qr_code:
            buffer, url = generate_equipment_qr_code(instance)
            filename = f"qr_welding_{instance.pk}_{uuid.uuid4().hex[:8]}.png"
            instance.qr_code.save(filename, File(buffer), save=True)
            buffer.close()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Payvandlash qurilmasi muvaffaqiyatli yaratildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        """Add request to serializer context for URL building"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Payvandlash qurilmalari"])
class WeldingEquipmentRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = WeldingEquipment.objects.all()
    serializer_class = WeldingEquipmentModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = WeldingEquipment.objects.get(pk=self.kwargs["pk"])
            return instance
        except WeldingEquipment.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos payvandlash qurilmasi mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )


# Isitish qozonlari
# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Isitish qozonlari"])
class HeatingBoilerListCreateAPIView(generics.ListCreateAPIView):
    queryset = HeatingBoiler.objects.order_by("-created_at")
    serializer_class = HeatingBoilerModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "detail_name"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        """Save the instance and generate QR code"""
        instance = serializer.save(author=self.request.user)

        if not instance.qr_code:
            buffer, url = generate_equipment_qr_code(instance)
            filename = f"qr_heating_{instance.pk}_{uuid.uuid4().hex[:8]}.png"
            instance.qr_code.save(filename, File(buffer), save=True)
            buffer.close()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Isitish qozonlari muvaffaqiyatli yaratildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        """Add request to serializer context for URL building"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Isitish qozonlari"])
class HeatingBoilerRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = HeatingBoiler.objects.all()
    serializer_class = HeatingBoilerModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = HeatingBoiler.objects.get(pk=self.kwargs["pk"])
            return instance
        except HeatingBoiler.DoesNotExist:
            raise NotFound(_("Bu id raqamga mos isitish qozoni mavjud emas"))

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )


# Yuk ko'tarish kranlari
# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Yuk ko'tarish kranlari"])
class LiftingCraneListCreateAPIView(generics.ListCreateAPIView):
    queryset = LiftingCrane.objects.order_by("-created_at")
    serializer_class = LiftingCraneModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "detail_name"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        """Save the instance and generate QR code"""
        instance = serializer.save(author=self.request.user)

        if not instance.qr_code:
            buffer, url = generate_equipment_qr_code(instance)
            filename = f"qr_lifting_{instance.pk}_{uuid.uuid4().hex[:8]}.png"
            instance.qr_code.save(filename, File(buffer), save=True)
            buffer.close()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Yuk ko'tarish kranlari muvaffaqiyatli yaratildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        """Add request to serializer context for URL building"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Yuk ko'tarish kranlari"])
class LiftingCraneRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = LiftingCrane.objects.all()
    serializer_class = LiftingCraneModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = LiftingCrane.objects.get(pk=self.kwargs["pk"])
            return instance
        except LiftingCrane.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos yuk ko'tarish krani mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )


# Bosim ostida sig'imlar
# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Bosim ostida sig'imlar"])
class PressureVesselListCreateAPIView(generics.ListCreateAPIView):
    queryset = PressureVessel.objects.order_by("-created_at")
    serializer_class = PressureVesselModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["company_name", "detail_name"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        """Save the instance and generate QR code"""
        instance = serializer.save(author=self.request.user)

        if not instance.qr_code:
            buffer, url = generate_equipment_qr_code(instance)
            filename = f"qr_pressure_{instance.pk}_{uuid.uuid4().hex[:8]}.png"
            instance.qr_code.save(filename, File(buffer), save=True)
            buffer.close()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "status": status.HTTP_201_CREATED,
                "message": "Bosim ostida sig'imi muvaffaqiyatli yaratildi",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_serializer_context(self):
        """Add request to serializer context for URL building"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


# ------------------------------------------------------------------------------------------
@extend_schema(tags=["Bosim ostida sig'imlar"])
class PressureVesselRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = PressureVessel.objects.all()
    serializer_class = PressureVesselModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsEquipmentMaster]

    def get_object(self):
        try:
            instance = PressureVessel.objects.get(pk=self.kwargs["pk"])
            return instance
        except PressureVessel.DoesNotExist:
            raise NotFound(
                _("Bu id raqamga mos bosim ostida sig'im mavjud emas")
            )

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_200_OK, "data": serializer.data}
        )
