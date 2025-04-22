from rest_framework import serializers

from apps.companies.models import Company


# serializers.py
class CompanyModelSerializer(serializers.ModelSerializer):
    logo = serializers.FileField(required=False)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "code",
            "address",
            "contact_email",
            "contact_phone",
            "logo",
            "is_active",
            "author",
        ]
