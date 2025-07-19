from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import LoginLog
from apps.users.models import User as UserType

User = get_user_model()


class UserSerializer(serializers.ModelSerializer[UserType]):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "name",
            "role",
            "image",
            "company",
            "phone_number",
            "email",
        ]


class LoginLogSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = LoginLog
        fields = ["id", "user", "device", "time"]


class TokenObtainSerializer(TokenObtainPairSerializer):
    jshshir = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    # Remove the username field from the parent class
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)

    def validate(self, attrs):
        jshshir = attrs.get("jshshir")
        password = attrs.get("password")

        user = get_user_model().objects.filter(jshshir=jshshir).first()

        if not user or not user.check_password(password):
            raise serializers.ValidationError(_("Hisob ma'lumotlari yaroqsiz"))

        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": str(user.role),
            "username": user.username,
            "name": user.name,
            "id": user.id,
        }

        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
