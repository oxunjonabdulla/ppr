from django.urls import path

from apps.users.api.views import CurrentUserAPIView, CustomTokenObtainPairView

app_name = "users"
urlpatterns = [
    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("user/me/", CurrentUserAPIView.as_view(), name="current-user"),
]
