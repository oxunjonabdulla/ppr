from django.db import transaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from apps.users.api.permissions import IsSuperUser
from apps.utils.paginator import StandardResultsSetPagination

from ..models import Company
from .serializers import CompanyModelSerializer


@extend_schema(tags=["Korxonalar"])
class CompanyListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.order_by("-created_at")
    serializer_class = CompanyModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "code"]
    pagination_class = StandardResultsSetPagination

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"status": status.HTTP_201_CREATED, "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


@extend_schema(tags=["Korxonalar"])
class CompanyRetrieveUpdateDestroyAPIView(
    generics.RetrieveUpdateDestroyAPIView
):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]

    def get_object(self):
        try:
            instance = Company.objects.get(pk=self.kwargs["pk"])
            return instance
        except Company.DoesNotExist:
            raise NotFound(_("Bu id raqamga mos korxona mavjud emas"))

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {"status": status.HTTP_204_NO_CONTENT, "data": serializer.data}
        )
