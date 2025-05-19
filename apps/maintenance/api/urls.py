from django.urls import path

from apps.maintenance.api.views import MaintenanceScheduleListCreateAPIView, \
    MaintenanceScheduleRetrieveUpdateDestroyAPIView, MaintenanceWarningListAPIView, \
    MaintenanceWarningRetrieveUpdateDestroyAPIView

urlpatterns = [
    path("maintenance-list-create/", MaintenanceScheduleListCreateAPIView.as_view(),name="maintenance-list-create"),
    path("maintenance-detail/<int:pk>/", MaintenanceScheduleRetrieveUpdateDestroyAPIView.as_view(),name="maintenance-detail"),
    # warnings
    path("maintenance-warning-list/", MaintenanceWarningListAPIView.as_view(), name="maintenance-warning-list"),
    path("maintenance-warning-detail/<int:pk>/", MaintenanceWarningRetrieveUpdateDestroyAPIView.as_view(), name="maintenance-warning-detail"),
]