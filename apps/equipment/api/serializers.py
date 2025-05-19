from rest_framework import serializers

from apps.equipment.models import (
    HeatingBoiler,
    LatheMachine,
    LiftingCrane,
    PressureVessel,
    WeldingEquipment,
)


class LatheMachineModelSerializers(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class Meta:
        model = LatheMachine
        fields = "__all__"


class WeldingEquipmentModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()

    class Meta:
        model = WeldingEquipment
        fields = "__all__"


class HeatingBoilerModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()


    class Meta:
        model = HeatingBoiler
        fields = "__all__"


class LiftingCraneModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()


    class Meta:
        model = LiftingCrane
        fields = "__all__"


class PressureVesselModelSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField()


    class Meta:
        model = PressureVessel
        fields = "__all__"
