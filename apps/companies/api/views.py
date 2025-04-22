from django.db import transaction
from django.shortcuts import get_object_or_404, render
from drf_spectacular.utils import extend_schema
from rest_framework import filters, generics, parsers, permissions, status
from rest_framework.response import Response

from apps.users.api.permissions import IsSuperUser
from apps.utils.paginator import StandardResultsSetPagination

from ..models import Company
from .serializers import CompanyModelSerializer


@extend_schema(tags=["Korxonalar"])
class CompaniesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.order_by("-created_at")
    serializer_class = CompanyModelSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "code"]
    pagination_class = StandardResultsSetPagination
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

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
