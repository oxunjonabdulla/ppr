from django.urls import path

from .views import CompaniesListCreateAPIView

urlpatterns = [
    path(
        "companies-list-create/",
        CompaniesListCreateAPIView.as_view(),
        name="companies-list-create",
    ),
]
