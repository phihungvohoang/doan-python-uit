from rest_framework import serializers
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "owner",
            "owner_name",
            "name",
            "address",
            "description",
            "total_floors",
            "created_at",
        ]
        read_only_fields = ["owner", "created_at"]