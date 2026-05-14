from rest_framework import serializers
from .models import Contract
from rooms.models import Room


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = "__all__"

    def validate(self, attrs):
        room = attrs.get("room")

        if room and room.status != Room.Status.AVAILABLE:
            raise serializers.ValidationError(
                "Phòng này hiện không trống, không thể tạo hợp đồng."
            )

        if attrs["end_date"] <= attrs["start_date"]:
            raise serializers.ValidationError(
                "Ngày kết thúc phải sau ngày bắt đầu."
            )

        return attrs