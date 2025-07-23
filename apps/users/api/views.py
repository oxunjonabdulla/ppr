from sys import exception

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api.permissions import IsEquipmentMaster
from apps.users.api.serializers import (
    LoginLogSerializer,
    LogoutSerializer,
    TokenObtainSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from apps.users.models import LoginLog

User = get_user_model()


@extend_schema(tags=["Users"])
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = User.objects.get(jshshir=request.data["jshshir"])
            device = request.headers.get("user-agent", "Unknown device")
            LoginLog.objects.create(user=user, device=device)
        return response


@extend_schema(tags=["Users"])
class CurrentUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@extend_schema(tags=["Users"])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # ✅ Only admin can see all users


@extend_schema(tags=["Users"])
class LoginLogListAPIView(ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logs = request.user.login_logs.all().order_by("-time")
        return Response({"results": LoginLogSerializer(logs, many=True).data})


@extend_schema(
    tags=["Users"], request=LogoutSerializer, responses={205: None, 400: dict}
)
class LogoutApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh_token = request.data["refresh"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Tizimdan muvaffaqiyatli chiqdingiz!"},
                status=status.HTTP_205_RESET_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": "Invalid token or already logged out."},
                status=status.HTTP_400_BAD_REQUEST,
                exception=e,
            )


@extend_schema(tags=["Users"])
class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsEquipmentMaster]
