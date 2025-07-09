from django.urls import path

from apps.users.api.views import (
    CurrentUserAPIView,
    CustomTokenObtainPairView,
    LoginLogListAPIView,
    UserListAPIView,
)

app_name = "users"
urlpatterns = [
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("user/me/", CurrentUserAPIView.as_view(), name="current-user"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path(
        "user/login-logs/",
        LoginLogListAPIView.as_view(),
        name="user-login-logs",
    ),
]
