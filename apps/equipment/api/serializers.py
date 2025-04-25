from rest_framework import serializers

from apps.equipment.models import (
    HeatingBoiler,
    LatheMachine,
    LiftingCrane,
    PressureVessel,
    WeldingEquipment,
)


class LatheMachineModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = LatheMachine
        fields = "__all__"


class WeldingEquipmentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeldingEquipment
        fields = "__all__"


class HeatingBoilerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatingBoiler
        fields = "__all__"


class LiftingCraneModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiftingCrane
        fields = "__all__"


class PressureVesselModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PressureVessel
        fields = "__all__"
