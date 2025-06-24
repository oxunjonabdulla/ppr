from django.urls import path

from apps.companies.api.views import (
    CompanyListCreateAPIView,
    CompanyRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "company-list-create/",
        CompanyListCreateAPIView.as_view(),
        name="company-list-create",
    ),
    path(
        "company-detail/<int:pk>/",
        CompanyRetrieveUpdateDestroyAPIView.as_view(),
        name="company-detail",
    ),
]
