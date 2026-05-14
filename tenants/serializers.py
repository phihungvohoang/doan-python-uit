from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            "id",
            "full_name",
            "phone",
            "identity_number",
            "date_of_birth",
            "address",
        ]