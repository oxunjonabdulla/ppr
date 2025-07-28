from django.urls import path

from apps.users.api.views import (
    CurrentUserAPIView,
    CustomTokenObtainPairView,
    LoginLogListAPIView,
    LogoutApiView,
    UserCreateAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    UserUpdateAPIView,
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
        "user-update/<int:pk>/",
        UserUpdateAPIView.as_view(),
        name="user-update",
    ),
    path(
        "user-delete/<int:pk>/",
        UserDeleteAPIView.as_view(),
        name="user-delete",
    ),
    path(
        "user/login-logs/",
        LoginLogListAPIView.as_view(),
        name="user-login-logs",
    ),
    path("user/create/", UserCreateAPIView.as_view(), name="user-create"),
    path("api/logout/", LogoutApiView.as_view(), name="logout"),
]
