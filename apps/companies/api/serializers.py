from rest_framework import serializers

from apps.companies.models import Company


# serializers.py
class CompanyModelSerializer(serializers.ModelSerializer):
    logo = serializers.FileField(required=False)

    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ["author", "created_at", "updated_at"]
