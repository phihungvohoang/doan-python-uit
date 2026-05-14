from rest_framework import serializers
from .models import UtilityReading, Invoice


class UtilityReadingSerializer(serializers.ModelSerializer):
    electric_fee = serializers.SerializerMethodField()
    water_fee = serializers.SerializerMethodField()

    class Meta:
        model = UtilityReading
        fields = [
            "id",
            "contract",
            "month",
            "year",
            "old_electric",
            "new_electric",
            "old_water",
            "new_water",
            "electric_price",
            "water_price",
            "electric_fee",
            "water_fee",
        ]

    def get_electric_fee(self, obj):
        return obj.electric_fee()

    def get_water_fee(self, obj):
        return obj.water_fee()

    def validate(self, attrs):
        if attrs["new_electric"] < attrs["old_electric"]:
            raise serializers.ValidationError(
                "Chỉ số điện mới không được nhỏ hơn chỉ số cũ."
            )

        if attrs["new_water"] < attrs["old_water"]:
            raise serializers.ValidationError(
                "Chỉ số nước mới không được nhỏ hơn chỉ số cũ."
            )

        return attrs


class InvoiceSerializer(serializers.ModelSerializer):
    tenant_name = serializers.CharField(
        source="contract.tenant.full_name",
        read_only=True
    )
    room_number = serializers.CharField(
        source="contract.room.room_number",
        read_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "contract",
            "tenant_name",
            "room_number",
            "month",
            "year",
            "room_fee",
            "electric_fee",
            "water_fee",
            "service_fee",
            "total_amount",
            "due_date",
            "status",
        ]

        read_only_fields = ["total_amount"]