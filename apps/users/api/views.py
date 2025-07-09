from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.api.serializers import (
    LoginLogSerializer,
    TokenObtainSerializer,
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
