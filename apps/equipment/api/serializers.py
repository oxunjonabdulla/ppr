from rest_framework import serializers

from apps.equipment.models import (
    Equipment,
    HeatingBoiler,
    LatheMachine,
    LiftingCrane,
    PressureVessel,
    WeldingEquipment,
)
from apps.users.api.serializers import UserSerializer
from apps.users.models import User


class LatheMachineModelSerializers(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer(read_only=True)
    responsible_person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsible_person",
        write_only=True,
    )
    qr_code = serializers.ImageField(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = LatheMachine
        fields = "__all__"

    def get_qr_code_url(self, obj):
        """Get full URL for QR code image"""
        if obj.qr_code:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class WeldingEquipmentModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer(read_only=True)
    responsible_person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsible_person",
        write_only=True,
    )
    qr_code = serializers.ImageField(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = WeldingEquipment
        fields = "__all__"

    def get_qr_code_url(self, obj):
        """Get full URL for QR code image"""
        if obj.qr_code:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class HeatingBoilerModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer(read_only=True)
    responsible_person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsible_person",
        write_only=True,
    )
    qr_code = serializers.ImageField(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = HeatingBoiler
        fields = "__all__"

    def get_qr_code_url(self, obj):
        """Get full URL for QR code image"""
        if obj.qr_code:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class LiftingCraneModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer(read_only=True)
    responsible_person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsible_person",
        write_only=True,
    )
    qr_code = serializers.ImageField(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = LiftingCrane
        fields = "__all__"

    def get_qr_code_url(self, obj):
        """Get full URL for QR code image"""
        if obj.qr_code:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class PressureVesselModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer(read_only=True)
    responsible_person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source="responsible_person",
        write_only=True,
    )
    qr_code = serializers.ImageField(read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = PressureVessel
        fields = "__all__"

    def get_qr_code_url(self, obj):
        """Get full URL for QR code image"""
        if obj.qr_code:
            request = self.context.get("request")
            if request:
                return request.build_absolute_uri(obj.qr_code.url)
            return obj.qr_code.url
        return None


class EquipmentPolymorphicSerializer(serializers.ModelSerializer):
    """Dynamically serialize the correct equipment subclass."""

    def to_representation(self, instance: Equipment):
        type_map = {
            "lathe_machine": LatheMachineModelSerializers,
            "welding_equipment": WeldingEquipmentModelSerializer,
            "heating_boiler": HeatingBoilerModelSerializer,
            "lifting_crane": LiftingCraneModelSerializer,
            "pressure_vessel": PressureVesselModelSerializer,
        }
        model_type = instance.type
        serializer_class = type_map.get(model_type)
        if serializer_class:
            return serializer_class(instance=instance.get_real_instance()).data
        return super().to_representation(instance)

    class Meta:
        model = Equipment
        fields = "__all__"
