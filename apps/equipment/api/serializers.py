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


class LatheMachineModelSerializers(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer()

    class Meta:
        model = LatheMachine
        fields = "__all__"


class WeldingEquipmentModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer()

    class Meta:
        model = WeldingEquipment
        fields = "__all__"


class HeatingBoilerModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer()

    class Meta:
        model = HeatingBoiler
        fields = "__all__"


class LiftingCraneModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer()

    class Meta:
        model = LiftingCrane
        fields = "__all__"


class PressureVesselModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class MinimalUserSerializer(UserSerializer):
        class Meta(UserSerializer.Meta):
            fields = ["id", "name", "username"]

        # --- For output (GET) ---

    responsible_person = MinimalUserSerializer()

    class Meta:
        model = PressureVessel
        fields = "__all__"


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
